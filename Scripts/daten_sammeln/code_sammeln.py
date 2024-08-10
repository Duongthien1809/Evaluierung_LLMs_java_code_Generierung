def get_code_from_solution(filename):
    with open(filename, 'r') as file:
        content = file.read()
        return content

#
# if __name__ == "__main__":
#     print(get_code_from_solution("../../Daten/LeetCode/Referenzen/java/g0001_0100/s0001_two_sum/Solution.java"))
