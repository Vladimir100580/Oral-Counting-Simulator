from random import randint
import time, datetime
nn = 5
# li = [['Jason', 10], ['John', 2], ['Jim', 9]]
# print(sorted(li, key=lambda x: x[1]))
datn = datetime.date.today()
o = '$'.join(map(str, (nn, datn, round(23.56) + 5, 23)))
print(o)
# k = 0
# mas = [4,5,8,6,3]
# print(mas[:k])
# for i in mas[:k]:
#        print(i)
#
#
#
# a = 16
#
# f = a / (7 ** 0.5)
# a = f * (7 ** 0.5)
# b = 0.5
# c = a ** b
# print(c)
# plase = 56
# print([['Вы стали ЧЕМПИОНОМ!!!', 'Вы заняли первое место!!!'][randint(0, 1)], 'Вы заняли ВТОРОЕ!!',
#        'Вы вошли в тройку сильнейших!', 'Вы вошли в семерку сильнейших.'][min(plase - 1, 3)])
#
# o = [2,3,4,7]
# p = [2,7,45,3]
# h = [3,9,2,4]
#
# f = []
# f += p
# f += h
# print(f)

# a = 7
# b = 7
# print (a == b != 7)
# ls = '34$4$0$0$89'
# lo = ['34', '4', '0', '0', '89']
#
# tts = sum(map(int, map(int, ls.split('$')[:4])))
# print(tts)
# print((1 or 1) and 0)
#
# print('Введите Фамилию, Имя, номер телефона, комментарий(в одно слово).')
# data = input("Через пробелы: ").split()
# if len(data) == 3:
#     data.append('-')
# if len(data) > 4:
#     data[3] = '_'.join(data[3:])
#     data = data[:4]
# data = ' '.join(data) + '\n'
#
# print(data)

#
# dict1 = {"a": 23, "b": 54}
#
# dict2 = {"d": 242, "c": 245}
#
# dict = {**dict1, **dict2}
# print(dict["a"], dict["c"])
#
# st = [12, 43, 65, 0, 53]
# print("$".join(list(map(lambda x: str(x), st))))
#
#
# strmas = list(map(lambda a: str(a), [1, 5, 6, 0, 0, 0, 0]))
# print(strmas)


# a = 250
#
# if a>200: print(1)
# elif a>20: print(2)
# elif a>0: print(3)
# else: print(4)
#
# proodin = [0]*5
# print(proodin)
#
#
# dic = {"12": 43, "45": "Акфы", "78": 123.6}
#
# print(dic)
# dic["12"] = 56
# print(dic)
#
# dic1 = {"71": "uiw4", "78": 92}
#
# dic.update(dic1)
# print(dic)
# print([3,4,5,6,7,8,9][2:4])
# sd = ["3", "4", "5", "6", "7"]
#
# print(list(enumerate(sd, 1)))

# a = 6
#
# y = 1 if a == 5 else 0
# print('y=', y)
#
# print(5 in range(1,5))
# st = '45,   -23 37'
# f = 0
# s = ''
# mas = []
# st = st + ' '
# for i in st:
#     if i.isdigit() or i == '-':
#         print('здесь ', i, s)
#         s += i
#         f = 1
#     else:
#         if f == 1:
#             mas.append(s)
#             s = ''
#             f = 0
# print(mas)


# p1 = ['gtnz']
#
# print('@%>$'.join(p1))
#
#
#
# o = [['sdfsdfs', '039'],['r5324yh','ds2']]
# for i in o[0][1]:
#     print(i, type(i), ord(i))
#
# s = []
# s.append(7)
# print(s)

# def gene(pol):
#     while True:
#         s = []
#         for i in range(6):
#             while True:
#                 k = randint(1, 9) * (2 * randint(0, 1) - 1)
#                 if k not in s and -k not in s:
#                     s.append(k)
#                     break
#         su = sum([p for p in s])
#         if sum([p / abs(p) for p in s if p > 0]) == pol and su != 0:
#             break
#     return s, su
#
#
# otvs = [[''] * 1 for i in range(60)]  # №задачи (кол-во вариантов -1), количество задач (№ коретжа)
# tasks = [[''] * 1 for i in range(60)]  # №задачи (кол-во вариантов -1), количество задач (№ коретжа)
# r=0
#
# # 56-57 (125 25)
# # 50 разность квадратов
# a = randint(112, 149)
# tasks[50][r] = str(a) + '²–' + str(a - 100) + '²='
# otvs[50][r] = str(((a - 100) * 2 + 100) * 100)
#
# # 51-52 разность квадратов через симметричные множители
# a = randint(2, 9) * 10
# b = randint(1, 3)
# while True:
#     c = randint(2, 9) * 10
#     if a != c: break
# d = randint(4, 7)
# if randint(0, 1) == 0:
#     tasks[51][r] = str(a - b) + '•' + str(a + b) + '='
# else:
#     tasks[51][r] = str(a + b) + '•' + str(a - b) + '='
# otvs[51][r] = str(a * a - b * b)
# if randint(0, 1) == 0:
#     tasks[52][r] = str(c - d) + '•' + str(c + d) + '='
# else:
#     tasks[52][r] = str(c + d) + '•' + str(c - d) + '='
# otvs[52][r] = str(c * c - d * d)
#
# # 53-55 6 разнознаковых
# s = [0 for i in range(3)]
# r1 = [0 for i in range(3)]
# while True:
#     for d in range(3):
#         q = gene(d + 2)
#         r1[d] = q[0]
#         s[d] = q[1]
#     if sum([p / abs(p) for p in s if p > 0]) == 1 \
#             and abs(s[0]) != abs(s[1]) and abs(s[0]) != abs(s[2]) and abs(s[1]) != abs(s[2]):
#         break
# st = ['' for i in range(3)]
# for n in range(3):
#     for m in r1[n]:
#         if m > 0 and m != r1[n][0]:
#             st[n] = st[n] + '+' + str(m)
#         else:
#             st[n] = st[n] + str(m)
# tasks[53][r] = st[0]
# otvs[53][r] = s[0]
# tasks[54][r] = st[1]
# otvs[54][r] = s[1]
# tasks[55][r] = st[2]
# otvs[55][r] = s[2]
#
# # 56-57 (125 25)
# i = randint(1, 4)  # (1-125,125 2-25,25 3-125,25(8) 4-125,25(4))
# if i == 1 or i == 2:
#     while True:
#         a = randint(2, 24)
#         b = randint(2, 24)
#         if a != b: break
#     while True:
#         a1 = randint(2, 12)
#         b1 = randint(2, 12)
#         if a1 != b1: break
#     d = [[a, b], [a1, b1]]
#     e = [4, 8]
#     c = 25 + (i - 1) * 100
#     if randint(0, 1) == 0:
#         tasks[56][r] = str(c) + '•' + str(400 + d[i - 1][0] * e[i - 1]) + '='
#     else:
#         tasks[56][r] = str(400 + d[i - 1][0] * e[i - 1]) + '•' + str(c) + '='
#     otvs[56][r] = str((400 + d[i - 1][0] * e[i - 1]) * c)
#
#     if randint(0, 1) == 0:
#         tasks[57][r] = str(c) + '•' + str(800 + d[i - 1][1] * e[i - 1]) + '='
#     else:
#         tasks[57][r] = str(800 + d[i - 1][1] * e[i - 1]) + '•' + str(c) + '='
#     otvs[57][r] = str((800 + d[i - 1][1] * e[i - 1]) * c)
#
# if i == 3:
#     while True:
#         a = randint(2, 24)
#         b = randint(2, 12)
#         if a != 2 * b and a != b:
#             break
#     for k in range(56, 58):
#         d = [a, b]
#         e = [4, 8]
#         c = (57 - k) * 100 + 25
#         if randint(0, 1) == 0:
#             tasks[k][r] = str(c) + '•' + str(800 + d[57 - k] * e[57 - k]) + '='
#         else:
#             tasks[k][r] = str(800 + d[57 - k] * e[57 - k]) + '•' + str(c) + '='
#         otvs[k][r] = str((800 + d[57 - k] * e[57 - k]) * c)
#
# if i == 4:
#     while True:
#         a = randint(2, 24)
#         b = randint(2, 12)
#         if a != 2 * b and a != b:
#             break
#     for k in range(56, 58):
#         d = [a, b]
#         e = [4, 8]
#         c = (57 - k) * 100 + 25
#         if randint(0, 1) == 0:
#             tasks[k][r] = str(c) + '•' + str(400 + d[57 - k] * e[57 - k]) + '='
#         else:
#             tasks[k][r] = str(400 + d[57 - k] * e[57 - k]) + '•' + str(c) + '='
#         otvs[k][r] = str((400 + d[57 - k] * e[57 - k]) * c)
#
# # 58 (распределит99)
# while True:
#     a = randint(1, 8) * 10 + randint(1, 8)
#     b = 99 - a
#     c = randint(1, 8) * 10 + randint(1, 9)
#     if a != b and a != c and b != c: break
# if randint(0, 1) == 0:
#     f = str(a) + '•' + str(c)
# else:
#     f = str(c) + '•' + str(a)
# if randint(0, 1) == 0:
#     g = str(b) + '•' + str(c)
# else:
#     g = str(c) + '•' + str(b)
# tasks[58][r] = f + '+' + g
# otvs[58][r] = str(a * c + b * c)
#
# # 59 (распределит101)
# while True:
#     a1 = randint(1, 8) * 10 + randint(2, 9)
#     b1 = 101 - a
#     c1 = randint(1, 8) * 10 + randint(1, 9)
#     if a1 != b1 and a1 != c1 and b1 != c1 and a1 != a and c1 != c: break
# if randint(0, 1) == 0:
#     f = str(a1) + '•' + str(c1)
# else:
#     f = str(c1) + '•' + str(a1)
# if randint(0, 1) == 0:
#     g = str(b1) + '•' + str(c1)
# else:
#     g = str(c1) + '•' + str(b1)
# tasks[59][r] = f + '+' + g
# otvs[59][r] = str(a1 * c1 + b1 * c1)
#
# for i in range(1, randint(20, 25)):
#     while True:
#         k1 = randint(50, 59)
#         k2 = randint(50, 59)
#         if k1 != k2: break
#     tasks[k1][r], tasks[k2][r] = tasks[k2][r], tasks[k1][r]
#     otvs[k1][r], otvs[k2][r] = otvs[k2][r], otvs[k1][r]
#
#
# for u in range(50,60):
#     print(tasks[u][0], otvs[u][0])
#
#

# def gene(pol):
#     while True:
#         s = []
#         for i in range(6):
#             while True:
#                 k = randint(1, 9) * (2 * randint(0, 1) - 1)
#                 if k not in s and -k not in s:
#                     s.append(k)
#                     break
#         su = sum([p for p in s])
#         if sum([p / abs(p) for p in s if p > 0]) == pol and su != 0:
#             break
#     return s, su

#
# s = [0 for i in range(3)]
# r = [0 for i in range(3)]
# while True:
#     for d in range(3):
#         q = gene(d + 2)
#         r[d] = q[0]
#         s[d] = q[1]
#     if sum([p / abs(p) for p in s if p > 0]) == 1 \
#             and abs(s[0]) != abs(s[1]) and abs(s[0]) != abs(s[2]) and abs(s[1]) != abs(s[2]):
#         break
# st = ['' for i in range(3)]
# for n in range(3):
#     for m in r[n]:
#         if m > 0 and m != r[n][0]:
#             st[n] = st[n] + '+' + str(m)
#         else:
#             st[n] = st[n] + str(m)
#
# print(st, s)

# t = [randint(1,9)*(2*randint(0, 1)-1) for i in range(10)]
# z = sum([p/abs(p) for p in t if p > 0])
# print(t, z)
#
# st = [str(i) for i in t if i < 0 and '+' + str(i) for i in t if i > 0]
#
# print('st=',st)
#
# print(''.join(t))
#
#
# l = [1,2,3,4,5]
# l.pop()
# print(l)
# t = [5] + [3] + ['d']
# print(t)
# print('12;23;43'.join(';'))
#
# a = 'sdferty54'
# print(a.split('d'))

# tt = [[] for i in range(5)]
# print(tt)
# mas = [0 for i in range(10)]
# print(mas)
# n = 0
# exp = 10**8
# while n < exp:
#     s = 0
#     k = 0
#     while s <= 9:
#         rn = randint(1, 6)
#         s = s + rn
#         k += 1
#     mas[k-1] += 1
#     n += 1
#     if n%100000 == 0:
#         print(mas)
# p = [i/exp for i in mas]
# print(p)

# h=[[5],[1],3,2,8,6]
# print(h.pop(2))
# i = h.index(8)
# print(i)
# h[1].append(['6',5,3])
#
#
# print(h, h[1][1][1])
#
# for a in range(6):
#     print(a)
#
# e="435$343$"
# print('el=', e.split('$')[1])
#
# sum = 600001.0
# if sum > 0:
#     t = ' очков.'
#     if (sum // 10) % 10 != 1:
#         if sum % 10 == 2 or sum % 10 == 3 or sum % 10 == 4: t = ' очка.'
#         if sum % 10 == 1: t = ' очко.'
#
#     txt1 = 'Поздравляем! Вы набрали: ' + str(sum) + t
#     tx = ['неплохо', 'совсем неплохо', 'очень хорошо', 'прекрасно', 'просто превосходно'][min(sum // 30000, 4)]
#     txt2 = 'Для первого раза - ' + tx + '!'
# else:
#     txt1 = 'Пока Вам не удалось набрать ни одного очка.'
#     txt2 = 'Одна - это лишь первая попытка. Успехов в дальнейшем.;)'
#
# print(txt1, txt2)
#
# mp = ['«Скажи мудрости: «Ты сестра моя!» и разум назови родным твоим.» Притчи Соломона 7:4',
#       '«Скудоумный высказывает презрение к ближнему своему; но разумный человек молчит.» Притчи Соломона 11:12',
#       '«Добрый разум доставляет приятность, путь же беззаконных жесток.» Притчи Соломона 13:16',
#       '«Всякий благоразумный действует с знанием, а глупый выставляет напоказ глупость.» Притчи Соломона 13:17',
#       '«Ухо, внимательное к учению жизни, пребывает между мудрыми.» Притчи Соломона 15:31',
#       '«Приобретение мудрости гораздо лучше золота, и приобретение разума предпочтительнее отборного серебра.» Притчи Соломона 16:16',
#       '«На разумного сильнее действует выговор, нежели на глупого сто ударов.» Притчи Соломона 17:10',
#       '«Лучше встретить человеку медведицу, лишенную детей, нежели глупца с его глупостью.» Притчи Соломона 17:12',
#       '«И глупец, когда молчит, может показаться мудрым, и затворяющий уста свои – благоразумным.» Притчи Соломона 17:28',
#       '«Сердце разумного приобретает знание, и ухо мудрых ищет знания.» Притчи Соломона 18:16',
#       '«Нехорошо душе без знания, и торопливый ногами оступится.» Притчи Соломона 19:2',
#       '«Кто приобретает разум, тот любит душу свою; кто наблюдает благоразумие, тот находит благо.» Притчи Соломона 19:8',
#       '«Главное — мудрость: приобретай мудрость, и всем имением твоим приобретай разум.» Притчи Соломона 4:7',
#       '«Невежды получают себе в удел глупость, а благоразумные увенчаются знанием» Притчи Соломона 14:18',
#       '«От всякого труда есть прибыль, а от пустословия только ущерб» Притчи Соломона 14:27',
#       '«У терпеливого человека много разума, а раздражительный выказывает глупость» Притчи Соломона 14:29',
#       '«Благоразумный видит беду и укрывается; а неопытные идут вперед и наказываются» Притчи Соломона 27:12',
#       '«Подарок тайный тушит гнев, и дар в пазуху – сильную ярость.» Притчи Соломона 21:14',
#       '«Помыслы в сердце человека – глубокие воды, но человек разумный вычерпывает их.» Притчи Соломона 20:5',
#       '«Кто хранит наставление, тот на пути к жизни; а отвергающий обличение – блуждает.» Притчи Соломона 10:17',
#       '«Мерзость перед Господом всякий надменный сердцем; можно поручиться, что он не останется ненаказанным.» Притчи Соломона 16:5',
#       '«Когда мудрость войдет в сердце твое, и знание будет приятно душе твоей, тогда рассудительность будет оберегать тебя, разум будет охранять тебя» Притчи Соломона 2:10-11',
#       '«Посему ходи путем добрых и держись стезей праведников.» Притчи Соломона 2:20',
#       '«Милость и истина да не оставляют тебя: обвяжи ими шею твою, напиши их на скрижали сердца твоего, и обретешь благоволение в очах Бога и людей.» Притчи Соломона 3:3-4',
#       '«Блажен человек, который снискал мудрость, и человек, который приобрел разум,...» Притчи Соломона 3:13',
#       '«Не отказывай в благодеянии нуждающемуся, когда рука твоя в силе сделать его.» Притчи Соломона 3:27',
#       '«Не замышляй против ближнего твоего зла, когда он без опасения живет с тобою.» Притчи Соломона 3:29',
#       '«Мудрые наследуют славу, а глупые - бесславие.» Притчи Соломона 3:35',
#       '«потому что мудрость лучше жемчуга, и ничто из желаемого не сравнится с нею.» Притчи Соломона 8:11',
#       '«Я - Мудрость, обитаю с Благоразумием. Я - Знание, меня можно найти в предосторожности.» Притчи Соломона 8:12',
#       '«оставьте неразумие, и живите, и ходите путем разума.» Притчи Соломона 9:6'
#       ]
#
# pr = mp[randint(0, len(mp) - 1)].split('Притчи')
# print(pr[1])
