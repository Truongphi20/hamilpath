import numpy as np
from module import sinequal as si
import argparse

# Initialize parser
parser = argparse.ArgumentParser()
 
# Adding optional argument
parser.add_argument("-t", "--vectors")
parser.add_argument("-v",'--version', action='version', version='%(prog)s 2.0',help = 'show version')


# Read arguments from command line
args = parser.parse_args()


def FindPoints(list_vec): #Find point in graph
    points = []
    tem_point = [points.extend(list(vector)) for vector in list_vec]
    points = list(set(points))
    #print(points)
    return sorted(points)

def Cre_Matrix(vectors, points): # Creating matrixes for vectors 
    # print(vectors)
    # print(sorted(points))
    matrixes = []
    for vector in vectors:
        pos_row = [0]*len(points)
        neg_row = [0]*len(points)

        pos_index = points.index(vector[1])
        neg_index = points.index(vector[0])

        pos_row[pos_index] += 1
        neg_row[neg_index] += 1

        matrixes.append(np.array([pos_row,neg_row]))
    # print(matrixes)
    return matrixes

def PrepareCo(matrixes): # Prepare coeffcient condition matrix
    # print(matrixes)
    flatten_matrix = []
    for array in matrixes:
        lis = array.tolist()
        tem = lis[0]+lis[1]
        flatten_matrix.append(tem)
    # print(flatten_matrix)
    # print(len(flatten_matrix))

    final_matrix = []
    for k in range(len(flatten_matrix[0])):
        # print(k)
        tem_row = []
        for i in range(len(flatten_matrix)):
            # print(-flatten_matrix[i][k])
            tem_row.append(-flatten_matrix[i][k])
            #print(tem_row)
        tem_row.append(1)
        final_matrix.append(tem_row)
    # print(final_matrix)
    return np.array(final_matrix)



def SolveMatrix(list_vec, points, matrixes): # Intializing matrix for solving
    sys_matrix = np.empty((0,len(list_vec)+1), int)
    #print(sys_matrix)
    for i in range(len(list_vec)): # Add postitive condition and lesser than 1
        tem_row = [0]*(len(list_vec)+1)
        tem_row[i] = 1
        #print(tem_row)

        less_row = [0]*(len(list_vec)+1)
        less_row[i] = -1
        less_row[-1] = 1
        #print(less_row)
        
        sys_matrix = np.append(sys_matrix,np.array([tem_row,less_row]),axis=0)
    #print(sys_matrix)

    sum_row = [1]*(len(list_vec)+1) # Add sum condition equal number of points
    sum_row[-1] = -len(points)+1

    neg_sum_row = [-1]*(len(list_vec)+1)
    neg_sum_row[-1] = len(points)-1

    sys_matrix = np.append(sys_matrix,np.array([sum_row,neg_sum_row]),axis=0)
    #print(sys_matrix)

    #print(matrixes)

    co_matrix = PrepareCo(matrixes)
    # print(co_matrix)

    total_matrix = np.append(sys_matrix,co_matrix, axis = 0)
    #print(total_matrix)
    

    return total_matrix

def CreatNguon(total_matrix,list_vec):
    init_nguon = [0]*len(total_matrix)
    init_nguon[len(list_vec)*2] = 1
    init_nguon[len(list_vec)*2+1] = 1
    #print(init_nguon)
    return init_nguon

def Solve_Coeff(list_vec, points, matrixes): # Solve vector coefficients
    
    het_matrix = SolveMatrix(list_vec, points, matrixes)
    # print(het_matrix)

    nguon_goc = CreatNguon(het_matrix,list_vec)
    # print(nguon_goc)

    order = list(range(len(list_vec)))
    #print(order)

    cuctri = [0]*len(list_vec)
    #print(cuctri)

    return si.SolveByMatrix(het_matrix, order, nguon_goc, cuctri)

def PhiMatrix(coeffs,points,matrixes):
    rs_matrix = []
    for coeff in coeffs:
        matrix_i = np.array([[0]*len(points),[0]*len(points)])
        for matrix, co in zip(matrixes,coeff):
            matrix_i += matrix*co
        rs_matrix.append(matrix_i)
    return rs_matrix

def ChangeVec(took_vectors,start_char,path):
    for vector in took_vectors:
        if vector[0] == start_char:
            path += vector[-1]
            took_vectors.remove(vector)
    # print(path)
    # print(took_vectors)
    return path, took_vectors

def FindPath(coe, ma, points):

    took_vectors = [list_vec[i] for i in range(len(list_vec)) if coe[i] == 1]
    # print(took_vectors)

    start_index = list(ma[0]).index(0)
    start_char = points[start_index]
    # print(start_char)

    end_index = list(ma[1]).index(0)
    end_char = points[end_index]
    # print(end_char)

    path = start_char
    path, took_vectors = ChangeVec(took_vectors,start_char,path)
    # print(path)
    # print(took_vectors)

    while path[-1] != end_char:
        path, took_vectors = ChangeVec(took_vectors,path[-1],path)
    # print(path)
    return path


def ColectPath(coeffs,rs_matrix,points):
    final_paths =  []
    lene = len(points)
    for coe, ma in zip(coeffs,rs_matrix):
        path = FindPath(coe, ma, points)
        # print(path)
        if len(path) == lene:
            final_paths.append(path)
    return final_paths

def PathThrough(list_vec):

    points = FindPoints(list_vec)
    # print(points)

    matrixes = Cre_Matrix(list_vec, points)
    # print(matrixes)

    coeffs = Solve_Coeff(list_vec,points,matrixes)
    # print(coeffs)

    rs_matrix = PhiMatrix(coeffs,points,matrixes)
    # print(rs_matrix)

    path = ColectPath(coeffs,rs_matrix,points)
    # print(path)
    return path


# list_vec = ['BA', 'AC', 'CB', 'BD', 'DC', 'CE', 'DE', 'DF', 'EF']
# list_vec = ['AC','CB','AB','BD','DC']
list_vec = args.vectors.split(',')

path = PathThrough(list_vec)
print(path)