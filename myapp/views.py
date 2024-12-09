from django.shortcuts import render
import sys
from io import StringIO
def index(request):
    if request.method == 'POST':
        families = {}
        for i in range(1, 7):
            values = request.POST.get(f'value{i}')
            print(values)
            if values:
                families[i] = list(values)
        print(families)
        result = process_families(families)
        return render(request, 'result.html', {'result': result})
    return render(request, 'index.html')



def process_families(families):

    captured_output = StringIO()
    sys.stdout = captured_output


    print('Семейство подмножеств номеров 1 по строкам [0,1] матрицы M:')
    print("S1 =", families[1], end='; ')
    print("S2 =", families[2], end='; ')
    print("S3 =", families[3], end='; ')
    print("S4 =", families[4], end='; ')
    print("S5 =", families[5], end='; ')
    print("S6 =", families[6], end='; \n')

    t0 = []

    def func(array):

        flag = False
        index = 0
        for i in range(len(array)):
            if array[i] not in t0:
                t0.append(array[i])
                index = i
                flag = True
                break
            else:
                continue

        return flag, index

    T = {}

    def init(fams, T):

        count = 0
        for arr in fams:
            flag, index = func(fams[arr])
            count += 1
            if flag == False:
                break
            T[count] = fams[arr][index]

        return count, T

    def get_key(val, my_dict):
        for key, value in my_dict.items():
            if val == value:
                return key

    def find_key_by_value_in_list(dictionary, target):
        for key, value_list in dictionary.items():
            if isinstance(value_list, list) and target in value_list:
                return key
        return None

    def check_for_dublicate(originalList):
        newList = []
        for i in originalList:
            if i not in newList:
                newList.append(i)

        return newList

    def dublicates_only(originalList):
        newList = []
        for i in originalList:
            if i in newList:
                newList.append(i)
        return newList

    def representator(num, T0, T_key):
        print()
        print(T_key + 1, ")Выбор представителя S" + str(num), " = T(?) ⊂ T" + str(T_key), sep='')
        print("Просмотр и дополнение списка 1 из Si<=" + str(num))
        L0 = families[num]
        i = 0
        goat_dict = {}
        ind = get_key(L0[i], T0)
        magic_L = 0
        magic_S = 0
        print("L0 = S" + str(num) + " = <", L0, ">; T(", L0[i], ") = S" + str(get_key(L0[i], T0)), sep='')
        while (L0[i] in T0[ind]):
            goat_num = L0[i]
            L0 = check_for_dublicate(L0 + families[ind])
            goat_dict[goat_num] = families[ind]
            i += 1
            ind = get_key(L0[i], T0)
            if ind == None:
                print("L" + str(i), " = L" + str(i - 1), " + S" + str(get_key(L0[i - 1], T0)), " = <", L0, "> = Lk; ",
                      L0[i], " ∉ T" + str(T_key), sep='')
                break
            else:
                print("L" + str(i), " = L" + str(i - 1), " + S" + str(get_key(L0[i - 1], T0)), " = <", L0, ">; T(",
                      L0[i], ") = S" + str(ind), sep='')
                magic_S = get_key(L0[i - 1], T0)
                magic_L = i - 1
        Lk = L0
        none_el = Lk[i]
        return str(none_el), goat_dict, magic_S, magic_L

    def replace_of_representator(new, old, goat_dict, counter, T_key, magic_S, magic_L, T):
        num = old
        T_old = T0.copy()
        T0[get_key(old, T0)] = new
        t_oldest = T0.copy()
        T0[len(T0) + 1] = num

        if num not in families[counter]:
            print(new, " ∈ L" + str(magic_L) + " ∪ S" + str(magic_S) + " = T(" + T_old[magic_S] + "); {" + str(
                new) + "} + T" + str(T_key) + " - {" + str(num) + "} = {" + str(
                t_oldest.values().__str__().split("(")[1].split(")")[0]) + "} = T" + str(T_key) + "';", sep='')
            print("S" + str(magic_S) + " = T(" + str(new) + ")")
            magic_L -= 2
            magic_S = get_key(families[counter][0], T0)
            T0.pop(counter)
            replace_of_representator(old, find_key_by_value_in_list(goat_dict, old), goat_dict, counter, T_key, magic_S,
                                     magic_L, T)
        else:
            print(new, " ∈ L" + str(magic_L) + " ∪ S" + str(magic_S) + " = T(" + T_old[magic_S] + "); {" + str(
                new) + "} + T" + str(T_key) + " - {" + str(num) + "} = {" + str(
                t_oldest.values().__str__().split("(")[1].split(")")[0]) + "} = T" + str(T_key) + "'';", sep='')
            print("S" + str(magic_S) + " = T(" + str(new) + ")")
            print(num, " ∈ L0" + " = S" + str(counter) + "; {" + str(num) + "} + " + "T" + str(T_key) + "' = {" + str(
                T0.values().__str__().split("(")[1].split(")")[0]) + "} = T" + str(T_key + 1) + "; S" + str(
                counter) + " = T(" + str(num) + ")", sep='')
        return T0

    def cycle(counter, T):
        T_key = 0
        while counter != len(families) + 1:
            new_el, goat_dict, magic_S, magic_L = representator(counter, T, T_key)
            old_el = find_key_by_value_in_list(goat_dict, new_el)
            print("\nЗамена представителя и расширение T" + str(T_key), sep='')
            T = replace_of_representator(new_el, old_el, goat_dict, counter, T_key, magic_S, magic_L, T)
            counter += 1
            T_key += 1

    counter, T0 = init(families, T)
    print("\n0) Инициализация T: ", end=' ')
    for i in range(counter - 1):
        print("S" + str(i + 1) + " = T(", T0[i + 1], ")", sep='', end='; ')
    print('T0 =', T0.values().__str__().split("(")[1].split(")")[0])
    cycle(counter, T0)
    print("\nОтвет: T =", T0.values().__str__().split("(")[1].split(")")[0])
    output = captured_output.getvalue()

    # Вернем stdout обратно на стандартный поток
    sys.stdout = sys.__stdout__
    return output

def result(request):
    return render(request, 'result.html')
