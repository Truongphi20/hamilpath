import numpy as np
import math

def check_int(num_tex): #Check xem text có phải số hay không
	res = False
	if num_tex.isnumeric() == True:
		res = True
	else:
		if num_tex.lstrip('-').isdigit() == True:
			res = True
	return res

#print(check_int("d3"))

def check_int_list(num_tex_list): #Check xem co phai list so hay khong
	res = True
	for element in num_tex_list:
		if check_int(element) == False:
			res = False
	return res

def find_index_int_list(listb): #Tim index cua list so trong list lon
	for i in range(len(listb)):
		if check_int_list(listb[i]) == True:
			break
	return i

def Make_bpts(bpt,biens): #Tao ma tran bat phuog trinh cho một bất phương trình 

	dau = -1
	if  len(bpt.split(">=")) == 2: #Dau = -1 khi <=, dau =1 khi >=, dau = 2 khi == 
		dau = 1
	elif len(bpt.split("==")) == 2:
		dau = 2
	#print(dau)

	#print(bpt)
	if dau == 1:
		he_bpt = bpt.split(">=")[0]
		fi = bpt.split(">=")[1]
	elif len(bpt.split("<=")) == 2:
		he_bpt = bpt.split("<=")[0]
		fi = bpt.split("<=")[1]
	else:
		he_bpt = bpt.split("==")[0]
		fi = bpt.split("==")[1]
	#print(he_bpt)
	#print(fi)

	he_duong = he_bpt.split("+")
	#print(he_duong)

	he_duong_filter = []
	for i in he_duong:
		he_duong_filter.append(i.split("-")[0])
	he_duong_filter[:] = [x for x in he_duong_filter if x] #Xoa thanh phan rong
	#print(he_duong_filter)


	he_am = he_bpt.split("-")
	if he_am[0][1::] != "-":
		he_am.pop(0)
	#print(he_am)

	he_am_filter = []
	for i in he_am:
		he_am_filter.append("-" + i.split("+")[0])
	he_am_filter[:] = [x for x in he_am_filter if x]
	#print(he_am_filter)

	total = he_duong_filter + he_am_filter
	#print(total)

	dic = []
	for i in range(len(total)):
		tem = []
		#print("*" in total[i])
		if ("*" in total[i]) == False:
			if total[i][0] == "-":
				tem = ["-1",total[i][1:]]
			else:
				tem = ["1",total[i]]
		else:
			tem = total[i].split("*")
		
		dic.append(tem)

	#print(dic)

	dic.append(dic.pop(find_index_int_list(dic)))

	#print(dic)

	#print(dic[-1][0].lstrip('-').isdigit())
	#dic[-1][0] = str(int(dic[-1][0])*int(dic[-1][1])) 

	bpt_final = [0]*len(biens)
	#print(bpt_final)


	for i in range(len(dic)):
		#print(i)
		index = -1
		for k in range(len(biens)):
			#print(k)
			if dic[i][1] == biens[k]:
				index = k
				bpt_final[index] = int(dic[i][0])

		#print(index)
	bpt_final.append(-int(fi))
	#print(bpt_final)

	rs = []
	if dau == 1 or dau == -1:
		rs = [np.array(bpt_final)*dau]
	else:
		rs = [np.array(bpt_final),np.array(bpt_final)*-1]

	return rs

def mak_hebpt_matrix(he_bpt_list,biens): #Tao matrix he so bat phuong trinh cho hệ bất phương trình
	#print(he_bpt_list)
	matri = []
	for i in range(len(he_bpt_list)):
		#print(i)
		matri.extend(Make_bpts(he_bpt_list[i],biens))
	matri = np.array(matri)
	return matri

def truy_nguon(he_bpt): # Truy nguồn gốc từ phương trình hay từ bpt
    nguon_goc = []
    for i in he_bpt:
        if len(i.split("<=")) == 2 or len(i.split(">=")) == 2:
            nguon_goc.append(0)
        else:
            nguon_goc.extend([1,1])
    return nguon_goc

#biens = ["a","b","P","c","G","k"] # Khai báo tên biến
#cuctri = [0,0,1,0,-1,0]	# Khai báo biến có phải cực trị (0: không phải, 1: cực đại, -1: cực tiểu)

def order_bien(bien,cuctri): # Tìm ra thứ tự triệt tiêu biến
    bien_lis = []
    cuctri_lis = []
    for i in range(len(cuctri)):
        if cuctri[i] == 0:
            bien_lis.append(i)
        else:
            cuctri_lis.append(i)
    return bien_lis + cuctri_lis

#print(order_bien(biens,cuctri))

def tieu_bien(index,he,nguon_goc): # Tiêu biến mang index tương ứng trong hệ

    # Tạo hàm cong các thành phần giữa hai list {[1,2],[10,20]} -> [10,40] 
    cong_2list = lambda l1,l2: [l1[i]+l2[i] for i in range(len(l1))]

    # Tạo một hàm tiêu biến với đầu vào là hệ bất phương trình và index tiêu biến, đầu ra là hệ sau tiêu biến

    index_cd = [i for i in range(len(he)) if he[i][index] > 0] #Index cac hang duong
    index_ca = [i for i in range(len(he)) if he[i][index] < 0] #Index cac hang am

    index_d = index_cd[0] # index của gốc dương 
    #print(index_d)

    index_a = index_ca[0] # index của gốc âm
    #print(index_a) 

    he_moi = []
    for k in range(len(he)):
        if k != index_d:
            if he[k][index] > 0:
                he_moi.append(cong_2list(he[k]*abs(he[index_a][index]/he[k][index]),he[index_a]))
            elif he[k][index] < 0:
                he_moi.append(cong_2list(he[k]*abs(he[index_d][index]/he[k][index]),he[index_d]))
            else:
                he_moi.append(he[k])
    #print(np.array(he_moi))
    return np.array(he_moi)

#print(tieu_bien(order[0],he))

def giai_bien(index,order,he,nguon_goc): # Giải ra list hệ tiêu biến của biến cần tìm với index tương ứng
    lap = [he]
    for  i in range(len(order)):
        if order[i] != index:  
            lap.append(tieu_bien(order[i],lap[-1],nguon_goc))
    return lap

def phogia(index,tieu_bien3): #từ index của biến còn lại và hàm tiêu biến xuất ra list giá trị 
    max_bien = []
    min_bien = []
    #print(tieu_bien3)
    for i in range(len(tieu_bien3)):
        if tieu_bien3[i][index] > 0:
            min_bien.append(float('%.6f' % (-tieu_bien3[i][-1]/ tieu_bien3[i][index])))
        elif tieu_bien3[i][index] < 0:
            max_bien.append(float('%.10f' % (-tieu_bien3[i][-1]/ tieu_bien3[i][index])))
    # print(max_bien)
    # print(min_bien)

    max_bien_value = math.floor(min(max_bien))
    # print(max_bien_value)

    min_bien_value = math.ceil(max(min_bien))
    # print(min_bien_value)

    return list(range(min_bien_value,max_bien_value+1))

#pho_gia_tri = phogia(index_giai,tieu_bien3)
#print(pho_gia_tri)

def thay_nghiem(he, indexes, vals): # Thay nghiem o cac bien voi index tuong ung de tao ra pho nghiem gia

	he_the = he.tolist()

	for i in range(len(indexes)):
		for k in range(len(he_the)):
			for j in range(len(he_the[0])):
				if j == indexes[i]:
					he_the[k][-1] += vals[i]*he_the[k][j] 
					he_the[k][j] = 0 # Thay xong cho bang 0
	return np.array(he_the)

def tach_key(string): #Tach key lop tren thanh key lop duoi {/10/3/2} --> [/10/3/2,/3/2,/2]
	bac = string.count("/")
	#print(bac)

	rs = []
	for i in range(1,bac+1):
		rs.append("/"+ string.split("/",i)[-1])
	return rs
#print(tach_key("/10/3/2"))

def order_tlv(order): #Tao list of list order tich luy {[0,3,4,5] --> [[5],[4,5],[3,4,5],[0,3,4,5]]}
	rs = []
	for i in range(1,len(order)+1):
		rs.append(order[(len(order)-i):(len(order)):])
	#print(rs)
	return rs

#print(order_tl([0,3,4,5]))

def Tra_kq_ct(lib_nghiem,order): #Tra ket qua nghiem co cuc tri
	list_key_rs = [i for i in lib_nghiem if len(i.split("/")) == len(order)+1]
	#print(list_key_rs)

	rs_final = []
	key_rs = []
	rs = []
	for j in range(len(list_key_rs)):
		key_rs = tach_key(list_key_rs[j])
		#print(key_rs)

		rs = [lib_nghiem[i] for i in key_rs]
		#print(rs)
		rs_final.append(rs)

	return rs_final

#print(Tra_kq_ct(lib_nghiem,order))

def re_order_ma(he,nguon_goc,order): # Sap xep lai thu tu hang, bt truoc, cuc tri sau
	bt = [he[i] for i in range(len(nguon_goc)) if nguon_goc[i] == 0]
	#print(bt)
	ct = [he[i] for i in range(len(nguon_goc)) if nguon_goc[i] == 1]
	#print(ct)

	rs = np.array(bt+ct)
	#print(rs)
	return rs

def call_ng(lib_ng, classa): # Goi nghiem su dung theo classa
	keys = [i for i in lib_ng if i.count('/') == classa]
	ng_sd = []
	for key in keys:
		tem = tach_key(key)
		ng_sd.append([lib_ng[i] for i in tem])
	return ng_sd, keys

def add_libtt(ct,lib_tt, order_tl, classa,ng_sd): # Them nghiem thu tu
	if classa not in lib_tt: 
		ct_s = ct[order_tl[-1][len(ct)-1-classa]]
		if ct_s == 0:
			lib_tt[classa] = "-"
		elif ct_s == 1:
			lib_tt[classa] = len(ng_sd)-1
		else:
			lib_tt[classa] = 0
	return lib_tt

def nearest(index, ct_bor): # Tra ve class cua bien cuc trij gan nhat
	i = 0
	while i <= index and i >= 0:
		if ct_bor[index-i] != 0:
			break
		i += 1
	return index - i
#print(nearest(1, [1, -1, 0, 0]))

def ClearLib_ng(tv,classa): # Clear cac thanh phan trong lib_ng lon hon class hoi ve
    keys = [key for key in tv]
    for key in keys:
        if key.count("/") >= classa:
            tv.pop(key)

    #print(tv)
    return tv

def ClearLib_tt(tv,classa): # Clear cac thanh phan trong lib_ng lon hon class hoi ve
    keys = [key for key in tv]
    for key in keys:
        if key >= classa:
            tv.pop(key)
    #print(tv)
    return tv

def Solve_Inequal(biens, cuctri, he_bpt):

	## Reperation
	nguon_goc = truy_nguon(he_bpt) # Nguon goc tu phuong trinh (1) hay bpt (0)
	#print(nguon_goc)

	order = order_bien(biens,cuctri) # Thu tu giai, uu tien giai bien cuc tri truoc
	#print(order)

	order_tl = order_tlv(order) # Thu tu index the vao de tim pho gia
	#print(order_tl)

	he = re_order_ma(mak_hebpt_matrix(he_bpt,biens),nguon_goc,order) # Tao ma tran tu he bpt
	# print(he)

	ct_bor = [cuctri[order_tl[-1][len(cuctri)-1-i]] for i in range(len(cuctri))] # list cuc tri theo order
	#print(ct_bor)

	lib_bp = giai_bien(order[-1],order,he,nguon_goc) # Thu vien he tieu bien lan luot cac bien theo order
	#print(lib_bp)


	## Calculation
	classa = 1
	pho = phogia(order[-1],lib_bp[-1]) # Pho cua bien cuc tri
	#print(pho)
	lib_ng = {"/"+str(i):pho[i] for i in range(len(pho))} #Them vao thu vien
	#print(lib_ng)
	lib_tt = {}
	#print(lib_tt)

	while classa <= len(lib_bp)-1 and classa > 0:
		#print(f'class: {classa}')
		#print(f'lib_ng: {lib_ng}')

		ng_sd, keys = call_ng(lib_ng,classa) # goi nghiem su dung
		#print(ng_sd)
		#print(keys)

		#print(classa)

		lib_tt = add_libtt(cuctri,lib_tt,order_tl,classa-1,ng_sd) # them thu tu vao lib thu tu
		#print(lib_tt)

		if lib_tt[classa-1] == "-": # Neu khong phai la cuc tri thi giai het

			tem = 0
			#print(ng_sd)
			for ng, key in zip(ng_sd,keys):
				#print(ng)
				#print(order_tl[classa-1])
				hr = thay_nghiem(lib_bp[len(lib_bp)-classa-1], order_tl[classa-1], ng)
				#print(hr)
				pho = phogia(order[len(order)-1-classa],hr)
				#print(f'phobth: {pho}')

				#print(classa)
				if len(pho) != 0:
					for i in range(len(pho)):
						lib_ng['/'+str(i) + key]  = pho[i]
				else:
					#print(1)
					tem += 1 

			if tem == len(ng_sd):
				if ct_bor[0] != 0: 
					#print(classa)
					classa = nearest(classa, ct_bor)
					#print(classa)
					k = lib_tt[classa] - ct_bor[classa]
					#print(f'k: {k}, {classa}')
					#print(lib_ng)
					#print(call_ng(lib_ng,classa+1)[0])
					if k < 0 or k > len(call_ng(lib_ng,classa+1)[0])-1:
						classa = classa -1 
					lib_tt[classa] = lib_tt[classa] - ct_bor[classa]
					#print(classa)
					lib_ng = ClearLib_ng(lib_ng,classa+2)
					lib_tt = ClearLib_tt(lib_tt,classa+1)
			classa += 1


		else:   # Neu la bien cuc tri can xet giai

			ng = ng_sd[lib_tt[classa-1]]
			key = keys[lib_tt[classa-1]]
			#print(f'ngct:{ng}')
			#print(key)

			hrct = thay_nghiem(lib_bp[len(lib_bp)-classa-1], order_tl[classa-1], ng)
			#print(hrct)
			phoct = phogia(order[len(order)-1-classa],hrct)
			#print(f'test{phogia(3,hrct)}')
			#print(f'phoct: {phoct}')

			#print(1)
			if len(phoct) == 0:
				#print(ng_sd)
				k = lib_tt[classa-1] - ct_bor[classa-1]
				if k < 0 or k > len(call_ng(ng_sd,classa+1)[0])-1:
					classa = classa -1
				#print(lib_tt)
				#print(f'{lib_tt[classa-1]}- {ct_bor[classa-1]}')
				lib_tt[classa-1] = lib_tt[classa-1] - ct_bor[classa-1]
				#print(f'lb la {lib_tt[classa-1]}')
				lib_ng = ClearLib_ng(lib_ng,classa+1)
				lib_tt = ClearLib_tt(lib_tt,classa)
			else:
				for i in range(len(phoct)):
					lib_ng['/'+str(i) + key]  = phoct[i]
				#print(lib_ng)
				classa += 1
		
	#print(Tra_kq_ct(lib_ng,order))
	return  [biens[index] for index in order], Tra_kq_ct(lib_ng,order)


def SolveByMatrix(matrix, order, nguon_goc, cuctri):
	order_tl = order_tlv(order) # Thu tu index the vao de tim pho gia
	#print(order_tl)

	# print(matrix)
	# print(nguon_goc)
	# print(order)

	he = re_order_ma(matrix,nguon_goc,order) # Tao ma tran tu he bpt
	# print(he)

	ct_bor = [cuctri[order_tl[-1][len(cuctri)-1-i]] for i in range(len(cuctri))] # list cuc tri theo order
	#print(ct_bor)

	lib_bp = giai_bien(order[-1],order,he,nguon_goc) # Thu vien he tieu bien lan luot cac bien theo order
	#print(lib_bp[0])


	## Calculation
	classa = 1
	pho = phogia(order[-1],lib_bp[-1]) # Pho cua bien cuc tri
	#print(pho)
	lib_ng = {"/"+str(i):pho[i] for i in range(len(pho))} #Them vao thu vien
	#print(lib_ng)
	lib_tt = {}
	#print(lib_tt)

	while classa <= len(lib_bp)-1 and classa > 0:
		#print(f'class: {classa}')
		#print(f'lib_ng: {lib_ng}')

		ng_sd, keys = call_ng(lib_ng,classa) # goi nghiem su dung
		#print(ng_sd)
		#print(keys)

		#print(classa)

		lib_tt = add_libtt(cuctri,lib_tt,order_tl,classa-1,ng_sd) # them thu tu vao lib thu tu
		#print(lib_tt)

		if lib_tt[classa-1] == "-": # Neu khong phai la cuc tri thi giai het

			tem = 0
			#print(ng_sd)
			for ng, key in zip(ng_sd,keys):
				#print(ng)
				#print(order_tl[classa-1])
				hr = thay_nghiem(lib_bp[len(lib_bp)-classa-1], order_tl[classa-1], ng)
				#print(hr)
				pho = phogia(order[len(order)-1-classa],hr)
				#print(f'phobth: {pho}')

				#print(classa)
				if len(pho) != 0:
					for i in range(len(pho)):
						lib_ng['/'+str(i) + key]  = pho[i]
				else:
					#print(1)
					tem += 1 

			if tem == len(ng_sd):
				if ct_bor[0] != 0: 
					#print(classa)
					classa = nearest(classa, ct_bor)
					#print(classa)
					k = lib_tt[classa] - ct_bor[classa]
					#print(f'k: {k}, {classa}')
					#print(lib_ng)
					#print(call_ng(lib_ng,classa+1)[0])
					if k < 0 or k > len(call_ng(lib_ng,classa+1)[0])-1:
						classa = classa -1 
					lib_tt[classa] = lib_tt[classa] - ct_bor[classa]
					#print(classa)
					lib_ng = ClearLib_ng(lib_ng,classa+2)
					lib_tt = ClearLib_tt(lib_tt,classa+1)
			classa += 1


		else:   # Neu la bien cuc tri can xet giai

			ng = ng_sd[lib_tt[classa-1]]
			key = keys[lib_tt[classa-1]]
			#print(f'ngct:{ng}')
			#print(key)

			hrct = thay_nghiem(lib_bp[len(lib_bp)-classa-1], order_tl[classa-1], ng)
			#print(hrct)
			phoct = phogia(order[len(order)-1-classa],hrct)
			#print(f'test{phogia(3,hrct)}')
			#print(f'phoct: {phoct}')

			#print(1)
			if len(phoct) == 0:
				#print(ng_sd)
				k = lib_tt[classa-1] - ct_bor[classa-1]
				if k < 0 or k > len(call_ng(ng_sd,classa+1)[0])-1:
					classa = classa -1
				#print(lib_tt)
				#print(f'{lib_tt[classa-1]}- {ct_bor[classa-1]}')
				lib_tt[classa-1] = lib_tt[classa-1] - ct_bor[classa-1]
				#print(f'lb la {lib_tt[classa-1]}')
				lib_ng = ClearLib_ng(lib_ng,classa+1)
				lib_tt = ClearLib_tt(lib_tt,classa)
			else:
				for i in range(len(phoct)):
					lib_ng['/'+str(i) + key]  = phoct[i]
				#print(lib_ng)
				classa += 1
		
	#print(lib_ng)
	return  Tra_kq_ct(lib_ng,order) 

"""
biens = ["h","l","c","w","b","p","n","S","W"] # Đặt ẩn tương ứng là lượng item lấy ở từng item
cuctri = [0,0,0,0,0,0,0,1,-1]

he_bpt = ["100*h+2200*l+350*c+192*w+70*b+200*p+333*n-W==0", # Tổng khối lượng hàng hóa phải bé hơn 3kg
            "W<=3000","W>=171",
            "150*h+500*l+60*c+30*w+100*b+500*p+40*n-S==0",
            "S>=251",
            "h>=0","l>=0","c>=0", # Các lượng item phải lớn hơn hoặc bằng 0
            "w>=0","b>=0","p>=0","n>=0"]
#print(len(giaihebpt(he_bpt,biens))) 
items_lay = Solve_Inequal(biens, cuctri, he_bpt)
print(items_lay)
"""

'''
biens = ["m","g","h","c"] # Khai báo tên biến
cuctri = [0,0,0,0]	# Khai báo biến có phải cực trị (0: không phải, 1: cực đại, -1: cực tiểu)
he_bpt = ["2*m+5*g+7*h+10*c<=1000","2*m+5*g+10*h+15*c<=500","4*m+8*g+11*h+19*c==977",
			"m>=1","g>=1","h>=1","c>=1"]

nghiem = Solve_Inequal(biens, cuctri, he_bpt)[1]
print(nghiem)
'''
"""
biens = ['a','b','c','d','e','f','g','h','i','M']
cuctri = [0,0,0,0,0,0,0,0,0,-1]

he_bpt = ['a>=0','b>=0','c>=0','d>=0','e>=0','f>=0','g>=0','h>=0','i>=0',
         'a<=1','b<=1','c<=1','d<=1','e<=1','f<=1','g<=1','h<=1','i<=1', #coefficient equal 0 or 1
         '1*a+2*b+2*c+3*d+1*e+1*f+1*g+2*h+2*i-M==0', #total path length is minima
         'a+b+c+d+e+f+g+h+i==5' #Sum equal point number minus 1
         ]

items_lay = Solve_Inequal(biens, cuctri, he_bpt)
print(items_lay)
"""

# biens = ['a','b','c','d','e','f','g','h','i']
# cuctri = [0,0,0,0,0,0,0,0,0]

# he_bpt = ['a>=0','b>=0','c>=0','d>=0','e>=0','f>=0','g>=0','h>=0','i>=0',
#          'a<=1','b<=1','c<=1','d<=1','e<=1','f<=1','g<=1','h<=1','i<=1', #coefficient equal 0 or 1
#          'a+b+c+d+e+f+g+h+i==5', #Sum equal point number minus 1
#          '0*a<=1',
#           'a<=1','c<=1','b+e<=1','d<=1','f+g<=1','h+i<=1', #line 1 of matrix
#           'b<=1','a+d<=1','c+f<=1','e+g+h<=1','i<=1', #line 2 of matrix
#          ]

# items_lay = Solve_Inequal(biens, cuctri, he_bpt)
# print(items_lay)

'''
biens = ['a','b','c','d']
cuctri = [0,0,0,0]

he_bpt = ['a>=0','b>=0','c>=0','d>=0',
         'a<=1','b<=1','c<=1','d<=1', #coefficient equal 0 or 1
         'a+b+c+d==3', #Sum equal point number minus 1
          'a<=1','b<=1','c<=1','d<=1', #line 1 of matrix
          'a+d<=1','b+c<=1' #line 2 of matrix
         ]

items_lay = Solve_Inequal(biens, cuctri, he_bpt)
print(items_lay)
'''