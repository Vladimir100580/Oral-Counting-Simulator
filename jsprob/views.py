import time, datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from random import randint
from .models import DataUser, Indexs
from django.contrib.auth import authenticate, login
import json


# def setcookie(request):
#
#     response = HttpResponse()
#     response.set_cookie('bookname0', 'Sherlock Holmes0')
#     response.set_cookie('bookname2', 'Sherlock Holmes2')
#     response.delete_cookie('bookname')
#     tts = request.COOKIES.get('bookname')
#     print(tts)
#     print('cookie', request.COOKIES)
#     return response


def hello(request):
    answer = request.GET
    try:
        er = request.session['ti_contr']
    except:
        request.session['ti_contr'] = time.time() - 4
    # a = abs(float(request.session['ti_contr']) - time.time())
    if abs(float(request.session['ti_contr']) - time.time()) < 3 and 'intlg' not in answer and 'reg' not in answer:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')

        tab = Indexs.objects.get(pk=1)
        koler = tab.ipskol.split('$')
        idus = tab.ips.split('$')

        if ip in idus:
            koler[idus.index(ip)] = str(int(float(koler[idus.index(ip)]) + 1))
        else:
            idus.append(ip)
            koler.append('1')
        stid = ''
        stkol = ''
        i = 0
        for idu in idus:
            if (i + 1) != len(idus):
                d = '$'
            else:
                d = ''
            stid = stid + str(idu) + d
            stkol = stkol + str(koler[i]) + d
            i += 1
        tab.ips = stid
        tab.ipskol = stkol
        tab.save()
        t = 5 / 0

    if 'intlg' in answer or 'reg' in answer:
        dayend()
        request.session['ti_contr'] = time.time() - 3
    else:
        request.session['ti_contr'] = time.time()

    user_id = request.user.username
    dat = Indexs.objects.get(id=1)
    datn = datetime.date.today()
    fl0 = '0'
    if (user_id != ''):
        nm = request.user.first_name.split('$#$%')
        if len(nm) == 4: fl0 = '1'
        nm = ', ' + nm[1]
        fl = 1
    else:
        nm = ''
        fl = 0
    p1 = Indexs.objects.get(id=1).pole1.split('@%>$')
    if len(p1) != 0 and dat.curdate == datn:
        fl1 = 1
        prit = ''
        st = ''
    else:
        prit = Prit4i().pr
        fl1 = 0
        st = 'border: 2px solid green;'
    if 'reg' in answer:
        dayend()
        return redirect('regist')
    if 'intlg' in answer:
        dayend()
        lg = answer.__getitem__('lg')
        if len(lg) < 3: return redirect('home')
        if User.objects.filter(username=lg).exists() == 1:
            user = authenticate(request, username=lg, password='4591423')
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'jsprob/nezar.html')
    return render(request, 'jsprob/priv.html', {'nm': nm, 'fl': fl, 'fl0': fl0, 'fl1': fl1,
                                                'p1': p1, 'prit': prit, 'st': st})


def regist(request):
    # return redirect('logout')
    if request.method == 'GET':
        answer = request.GET
        if 'fam' in answer and 'name' in answer and 'lg' in answer:
            f = answer.__getitem__('fam').replace(' ', '').capitalize()
            n = answer.__getitem__('name').replace(' ', '').capitalize()
            if f == '' or n == '': return redirect('regist')
            k = answer.__getitem__('kl').replace(' ', '')
            lg = answer.__getitem__('lg')
            if len(f) < 2 or len(n) < 2 or len(f) > 25 or len(n) > 25 or len(k) > 25 or len(lg) > 30 or len(lg) < 3:
                return redirect('regist')
            if User.objects.filter(username=lg).exists():
                return render(request, 'jsprob/ujuse.html')
            else:
                DataUser(log=lg, scores=0, fik=f + ' ' + n + ' ' + k).save()
                user = User.objects.create_user(lg, '', '4591423', first_name=f + '$#$%' + n + '$#$%' + k)
                user.save()
                user = authenticate(request, username=lg, password='4591423')
                login(request, user)
                return render(request, 'jsprob/uspreg.html')
    return render(request, 'jsprob/registr.html')


def dayend():
    dat = Indexs.objects.get(id=1)
    datn = datetime.date.today()
    if dat.curdate != datn:
        lastday = dat.curdate
        dat.curdate = datn
        dat.save(update_fields=['curdate'])
        masd = DataUser.objects.order_by('-scorTD').filter(scorTD__gt=0).values_list('id', 'fik', 'scorTD')
        masd7 = masd[:min(7, len(masd))]
        for p in masd7:
            kar = DataUser.objects.get(id=p[0])
            kar.quanttop = kar.quanttop + 1
            if p == masd7[0]:
                kar.quantwin = kar.quantwin + 1
                p1 = Indexs.objects.get(id=1).pole1.split('@%>$')
                if len(p1) >= 3:
                    p1.pop()
                    p1 = '@%>$'.join([lastday.strftime('%d.%m.%Y') + ': ' + p[1] + ' (' + str(p[2]) + ')'] + p1)
                else:
                    p1 = lastday.strftime('%d.%m.%Y') + ': ' + p[1] + ' (' + str(p[2]) + ')' + '@%>$' + '@%>$'.join(p1)
                Indexs.objects.filter(id=1).update(pole1=p1)
            kar.scorTD = 0
            kar.save()
        for p in DataUser.objects.filter(scorTD__gt=0):
            p.scorTD = 0
            p.save(update_fields=['scorTD'])
        for p in DataUser.objects.filter(poptd__gt=0):
            p.poptd = 0
            p.save(update_fields=['poptd'])


def progress(request):
    usna = request.user.username
    if (usna is None) or (usna == ''):
        return redirect('home')
    kar = DataUser.objects.get(log=usna)
    popt = kar.pop
    if popt < 1: return render(request, 'jsprob/gogo.html')
    scl = []
    scl.append([1, kar.scoresl1])
    scl.append([2, kar.scoresl2])
    scl.append([3, kar.scoresl3])
    scl.append([4, kar.scoresl4])
    scl.append([5, kar.scoresl5])
    scl.append([6, kar.scoresl6])
    na4pops = int(float(kar.pole1.split('$')[0]))  # начато игр в сезоне
    popsez = int(float(kar.pole1.split('$')[1]))  # проёдено игр в сезоне
    na4popt = int(float(kar.pole1.split('$')[2]))  # начато игр за все время
    if kar.scorTD != 0:
        sctd = str(kar.scorTD) + ' (' + str(len(DataUser.objects.filter(scorTD__gt=kar.scorTD)) + 1) + orf1(
            kar.scorTD) + ' место)'
    else:
        sctd = '—'

    fl = 0
    if popsez >= 10: fl = 1
    pot = 0
    if fl == 1:
        for p in scl:
            pot += p[1]
    data = {
        'gls': kar.res1,
        'gls1': orf1(kar.res1),
        'scl': scl,
        'sezsc': kar.scores,
        'sezsc1': orf1(kar.scores),
        'sctd': sctd,
        'sctd1': orf1(kar.scorTD),
        'pozgl': len(DataUser.objects.filter(res1__gt=kar.res1)) + 1,
        'pozsez': len(DataUser.objects.filter(scores__gt=kar.scores)) + 1,
        'poztd': len(DataUser.objects.filter(scorTD__gt=kar.scorTD)) + 1,
        'quantwin': kar.quantwin,
        'quantwin1': orf(kar.quantwin),
        'quanttop': kar.quanttop,
        'quanttop1': orf(kar.quanttop),
        'pot': pot,
        'fl': fl,
        'popt': popt,
        'na4pops': na4pops,
        'na4popt': na4popt,
        'popsez': popsez,
        'popt1': orf(popt),
        'na4pops1': orf(na4pops),
        'na4popt1': orf(na4popt),
        'popsez1': orf(popsez),
    }
    return render(request, 'jsprob/progress.html', data)


def orf(sum):
    t = ' раз'
    if (sum // 10) % 10 != 1:
        if sum % 10 == 2 or sum % 10 == 3 or sum % 10 == 4: t = ' раза'
    return t


def orf1(sum):
    t = ' очков'
    if (sum // 10) % 10 != 1:
        if sum % 10 == 2 or sum % 10 == 3 or sum % 10 == 4: t = ' очка'
        if sum % 10 == 1: t = ' очко'
    return t


def itog(request):
    dayend()
    ud = request.COOKIES.get('lelrec15').split('$')
    if ud[0] != 'e':
        if float(ud[0]) < float(ud[1]):
            DataUser.objects.filter(log=request.session['ustns4usen']).update(scoresl5=ud[1])
    usna = request.session['ustns4usen']
    if (usna == None): return redirect('home')
    tts = request.COOKIES.get('totsumm').split('(#)$)')
    bonz = int(float(tts[2]) * 100)
    sum = int(float(tts[0])) + bonz
    bon = ' 100 X ' + str(int(float(tts[2]))) + ':'
    tx = ['неплохо', 'совсем неплохо', 'очень хорошо', 'прекрасно', 'просто превосходно'][min(sum // 70000, 4)]
    tt = DataUser.objects.get(log=usna)
    if tt.pole2 == '0':
        tt.pop = tt.pop + 1
        tt.poptd = tt.poptd + 1
        popmas = tt.pole1.split(
            '$')  # pole1 = Попыток в сезоне $ Пройдено игр в сезоне $ Попыток всего  pop - попыток всего
        popmas[1] = str(int(float(popmas[1]) + 1))
        tt.pole1 = '$'.join(popmas)
        tt.save()

    txt = txt1 = txt2 = txt3 = txt4 = txt5 = txt6 = ''
    ds = 0
    dsd = 0
    scold = 0
    scoldd = 0
    t = orf1(sum)
    txx = 'что — '
    if tt.pop == 1: txx = 'что, для первого раза — '

    if sum > 0:
        txt1 = "Вы набрали " + str(sum) + t + ', ' + txx + tx + '.'
    scolddt = tt.scorTD
    scoldd = tt.res1
    scold = tt.scores  # в этапах sclvus
    ds = int(float(sum) - scold)  # сравнение с рекордом сезона
    dsd = int(float(sum) - scoldd)  # сравнение с абсолютным рекордом
    if tt.pole2 == '0' and sum > 0 and tt.pop != 1 and popmas[1] != '1':
        mas0 = [i for i in
                DataUser.objects.filter(scores__gt=scold).order_by('-scores').values_list('scores', 'fik')]
        mas1 = [i for i in
                DataUser.objects.filter(scores__gt=sum).order_by('-scores').values_list('scores', 'fik')]

        mas01 = [i for i in
                 DataUser.objects.filter(res1__gt=scoldd).order_by('-res1').values_list('res1', 'fik')]
        mas11 = [i for i in
                 DataUser.objects.filter(res1__gt=sum).order_by('-res1').values_list('res1', 'fik')]
        mas02 = [i for i in
                 DataUser.objects.filter(scorTD__gt=scolddt).order_by('-scorTD').values_list('scorTD', 'fik')]
        mas12 = [i for i in
                 DataUser.objects.filter(scorTD__gt=sum).order_by('-scorTD').values_list('scorTD', 'fik')]

        txt = ''
        txt1 = "Вы набрали " + str(sum) + t + ', ' + txx + tx
        if ds > 0 and dsd > 0:
            DataUser.objects.filter(log=usna).update(scores=sum, res1=sum, pravil=(int(float(tts[1]) + float(tts[2]))),
                                                     bezosh=tts[2])
            txt = "ПОЗДРАВЛЯЕМ!!!!!"
            if ds == dsd:
                txt2 = "Тем самым побили свои рекорды, как абсолютный, так и Ваш рекорд в текущем" \
                       " сезоне на " + str(ds) + ". (" + str(scoldd) + " --> " + str(sum) + ")"
            else:
                txt2 = "Тем самым побили свой абсолютный рекорд на " + str(dsd) + " и Ваш рекорд в текущем" \
                                                                                  " сезоне на " + str(ds) + "."
        if ds > 0 and dsd == 0:
            DataUser.objects.filter(log=usna).update(scores=sum, pravil=(int(float(tts[1]) + float(tts[2]))),
                                                     bezosh=tts[2])
            txt = "ПОЗДРАВЛЯЕМ!!!"
            txt2 = "Тем самым побили свой рекорд текущего сезона на " + str(ds) + ". (" + str(scold) + " --> " \
                   + str(sum) + "). И повторили свой абсолютный рекорд"
        if ds > 0 and dsd < 0:
            DataUser.objects.filter(log=usna).update(scores=sum, pravil=(int(float(tts[1]) + float(tts[2]))),
                                                     bezosh=tts[2])
            txt = "ПОЗДРАВЛЯЕМ!!"
            txt2 = "Тем самым побили свой рекорд текущего сезона на " + str(ds) + ". До Вашего личного рекорда" \
                                                                                  " не хватило набрать " + str(
                abs(dsd)) + '.'

        pos_old = int(len(mas0) + 1)
        pos_now = int(len(mas1) + 1)

        if ds > 0:
            if pos_now < 11:
                if pos_old == pos_now:
                    if txt == '': txt = "Поздравляем!"
                    if pos_now != 1:
                        txt3 = 'и еще прочнее укрепились на ' + str(pos_now) + '-позиции в TOP-10 сезона.'
                    else:
                        txt3 = 'и еще сильнее утвердили свое ЛИДЕРСТВО в текущем сезоне.'
                else:
                    if pos_old > 10:
                        if pos_now != 1:
                            if txt == '': txt = 'ПОЗДРАВЛЯЕМ!'
                            txt3 = 'и на данный момент Вы вошли в TOП-10 сезона! \
                                     ( ' + str(pos_now) + ' место )'
                        else:
                            if txt == '': txt = 'ПОЗДРАВЛЯЕМ!!!'
                            txt3 = 'и на данный момент Вы врываетесь в ТОП-10 и становитесь ЧЕМПИОНОМ сезона.'
                    else:
                        if pos_now != 1:
                            if txt == '': txt = 'ПОЗДРАВЛЯЕМ!'
                            txt3 = 'и улучшили свою позицию в TOП-10 сезона. ( ' + \
                                   str(pos_old) + ' --> ' + str(pos_now) + ' )'
                        else:
                            if txt == '': txt = 'ПОЗДРАВЛЯЕМ!!!'
                            txt3 = 'и на данный момент Вы становитесь ЧЕМПИОНОМ сезона!'
            else:
                if pos_old != pos_now:
                    txt3 = ' и Ваше место в TOП-е сезона стало выше. ( ' + \
                           str(pos_old) + ' --> ' + str(pos_now) + ' )'

            pos_old = int(len(mas01) + 1)
            pos_now = int(len(mas11) + 1)

            if pos_now < 11:
                if pos_old == pos_now:
                    if txt == '': txt = "Поздравляем!"
                    if pos_now != 1:
                        txt4 = 'также еще прочнее укрепились на ' + str(pos_now) + '-позиции глобального TOP-10.'
                    else:
                        txt4 = 'также еще сильнее утвердили свое ЛИДЕРСТВО в игре.'
                else:
                    if pos_old > 10:
                        if pos_now != 1:
                            if txt == '': txt = 'ПОЗДРАВЛЯЕМ!'
                            txt4 = 'также на данный момент Вы вошли абсолютный TOП-10! \
                                     ( ' + str(pos_now) + ' место )'
                        else:
                            if txt == '': txt = 'ПОЗДРАВЛЯЕМ!!!'
                            txt4 = 'На данный момент Вы врываетесь в глобальный ТОП-10 и становитесь ЧЕМПИОНОМ!!'
                    else:
                        if pos_now != 1:
                            if txt == '': txt = 'ПОЗДРАВЛЯЕМ!'
                            txt4 = 'также улучшили свою позицию в глобальном TOП-10. ( ' + \
                                   str(pos_old) + ' --> ' + str(pos_now) + ' )'
                        else:
                            if txt == '': txt = 'ПОЗДРАВЛЯЕМ!!!'
                            txt4 = ' также на данный момент Вы становитесь абсолютным ЧЕМПИОНОМ!'
            else:
                if pos_old != pos_now:
                    txt4 = 'также Ваше место в TOП-е сезона стало выше. ( ' + \
                           str(pos_old) + ' --> ' + str(pos_now) + ' )'

        else:
            tvs = ''
            if float(sum) > scold * .98: tvs = ' совсем чуть-чуть '
            txt3 = 'Однако, до Вашего рекорда в сезоне не хватило' + tvs + ': ' + str(abs(ds)) + '.'
            if float(sum) == scold:
                txt = 'Поздравляем.'
                txt3 = 'Вы в точности повторили свой рекорд в текущем сезоне.'

        if tt.poptd != 1:
            scoldtd = tt.scorTD
            dsTD = int(float(sum) - tt.scorTD)
            if dsTD > 0:

                DataUser.objects.filter(log=usna).update(scorTD=sum)
                txt5 = "Вы побили свой рекорд сегодняшнего дня на " + str(dsTD) + ". (" + str(scoldtd) + " --> " \
                       + str(sum) + ")"

                pos_old = int(len(mas02) + 1)
                pos_now = int(len(mas12) + 1)

                if pos_now < 8:
                    if pos_old == pos_now:
                        if txt == '': txt = "Поздравляем!"
                        if pos_now != 1:
                            txt6 = 'и еще прочнее укрепились на ' + str(pos_now) + '-позиции TOP-7 дня.'
                        else:
                            txt6 = 'и еще сильнее утвердили свое лидерство в ТОР-е дня.'
                    else:
                        if pos_old > 7:
                            if pos_now != 1:
                                if txt == '': txt = 'Поздравляем!'
                                txt6 = 'На данный момент Вы вошли в сегодняшний TOП-7! \
                                                 ( ' + str(pos_now) + ' место )'
                            else:
                                if txt == '': txt = 'Поздравляем!'
                                txt6 = 'На данный момент Вы становитесь лидером ТОП-7 дня.'
                        else:
                            if pos_now != 1:
                                if txt == '': txt = 'Поздравляем!'
                                txt6 = 'и улучшили свою позицию в сегодняшнем TOП-7. ( ' + \
                                       str(pos_old) + ' --> ' + str(pos_now) + ' )'
                            else:
                                if txt == '': txt = 'Поздравляем!'
                                txt6 = 'На данный момент Вы становитесь лидером ТОП-7 дня.'
                else:
                    if pos_old != pos_now:
                        txt6 = 'Ваше место в TOП-е дня стало выше. ( ' + \
                               str(pos_old) + ' --> ' + str(pos_now) + ' )'
        else:
            mas1 = [i for i in
                    DataUser.objects.filter(scorTD__gt=sum).order_by('-scorTD').values_list('scorTD', 'fik')]
            pos_now = int(len(mas1) + 1)
            DataUser.objects.filter(log=usna).update(scorTD=sum)
            if pos_now > 7:
                txt6 = 'Теперь Ваша позиция в TOП-е дня: ' + str(pos_now) + '.'
            if 1 < pos_now < 8:
                if txt == '': txt = 'Поздравляем!'
                txt6 = 'На данный момент Вы вошли в TOП-7 сегодняшего дня: ( ' + str(pos_now) + ' место )'
            if pos_now == 1:
                if txt == '': txt = 'Поздравляем!!!'
                txt6 = 'На данный момент Вы становитесь лидером ТОП-7 дня.'

    else:
        if sum == 0:
            if tt.pop == 1:
                txt1 = 'УВЫ. Вам не удалось набрать ни одного балла.'
                txt2 = 'Однако, так как это Ваша первая попытка, дарим Вам 500 поощрительных очков.'
                DataUser.objects.filter(log=usna).update(scores=500)
            else:
                if popmas[1] == '1':
                    txt1 = 'УВЫ. Вам не удалось набрать ни одного балла.'
                    txt2 = 'Однако, так как это Ваша первая попытка в этом сезоне, дарим Вам 500 поощрительных очков.'
                    DataUser.objects.filter(log=usna).update(scores=500)
                else:
                    txt1 = 'УВЫ. Вам не удалось набрать ни одного балла.'
                    txt2 = 'Полагаем, Вы просто решили проверить, что произойдет?'
                    txt3 = 'Как видите — ничего особо страшного.'
        if sum != 0 and tt.pole2 == '0':
            mas1 = [i for i in
                    DataUser.objects.filter(scores__gt=sum).order_by('-scores').values_list('scores', 'fik')]
            pos_now = int(len(mas1) + 1)
            if pos_now > 10:
                txt5 = 'В ТОП-е сезона Вы пока занимаете: ' + str(pos_now) + ' позицию.'
            if 1 < pos_now < 11:
                if txt == '': txt = 'ПОЗДРАВЛЯЕМ!'
                txt5 = 'На данный момент Вы вошли в TOП-10 текущего сезона: ( ' + str(pos_now) + ' место )'
            if pos_now == 1:
                if txt == '': txt = 'ПОЗДРАВЛЯЕМ!!!!'
                txt5 = 'На данный момент Вы становитесь лидером ТОП-10 сезона.'
            if dsd > 0:
                p = sum
            else:
                p = tt.res1

            mas1 = [i for i in
                    DataUser.objects.filter(scorTD__gt=sum).order_by('-scorTD').values_list('scorTD', 'fik')]
            pos_now = int(len(mas1) + 1)
            DataUser.objects.filter(log=usna).update(scorTD=sum)
            if txt5 != '':
                txtdop = 'и '
            else:
                txtdop = 'На данный момент Вы '
            if pos_now > 7:
                txt6 = 'Теперь Ваша позиция в TOП-е дня: ' + str(pos_now) + '.'
            if 1 < pos_now < 8:
                if txt == '': txt = 'Поздравляем!'
                txt6 = txtdop + ' вошли в TOП-7 сегодняшего дня: ( ' + str(pos_now) + ' место )'
            if pos_now == 1:
                if txt == '': txt = 'Поздравляем!!!'
                txt6 = txtdop + ' становитесь лидером ТОП-7 дня.'

            DataUser.objects.filter(log=usna).update(scores=sum, scorTD=sum, res1=p,
                                                     pravil=(int(float(tts[1]) + float(tts[2]))), bezosh=tts[2])

    pr = Prit4i().pr
    DataUser.objects.filter(log=usna).update(pole2='1')
    return render(request, 'jsprob/itog.html', {'txt': txt, 'txt1': txt1, 'txt2': txt2, 'txt3': txt3,
                                                'txt4': txt4, 'txt5': txt5, 'txt6': txt6, 'txt7': pr[0],
                                                'txt8': pr[1], 'pr': int(float(tts[1]) + float(tts[2])),
                                                'bz': int(float(tts[2])), 'lv1': tts[3], 'lv2': tts[4], 'lv3': tts[5],
                                                'lv4': tts[6], 'lv5': tts[7],
                                                'bon': bon, 'bonz': bonz, 'su': str(sum - bonz)})


def toptab(request):
    dayend()
    tt = []
    try:
        usna = request.user.first_name.replace('$#$%', ' ')
    except:
        usna = ''
    n = 0
    for r in DataUser.objects.order_by('-scores'):
        if r.scores != 0:
            n += 1
            fio = str(n) + ') ' + r.fik
            if r.fik != usna:
                col = str(n % 3)
            else:
                col = '3'
            tt.append([col, fio, r.scores, str(r.pravil) + '/' + str(r.bezosh)])
    return render(request, 'jsprob/toptab.html', {'tt': tt})


def toplvl(request):
    tt = [[] for i in range(6)]
    try:
        usna = request.user.first_name.replace('$#$%', ' ')
    except:
        usna = ''
    n = 0
    m = 0
    for l in range(6):
        n = 0
        m += 1
        tt[m - 1].append(m)
        for r in DataUser.objects.order_by('-scoresl' + str(m)).values_list('fik', 'scoresl' + str(m))[:10]:
            if r[1] != 0:
                n += 1
                if r[0] != usna:
                    col = str(n % 3)
                else:
                    col = '3'
                tt[m - 1].append([col, str(n) + ') ' + r[0], r[1]])
    return render(request, 'jsprob/toplvl.html', {'tt': tt})


def topday(request):
    tt = []
    try:
        usna = request.user.first_name.replace('$#$%', ' ')
    except:
        usna = ''
    n = 0
    for r in DataUser.objects.order_by('-scorTD'):
        if r.scorTD != 0:
            n += 1
            fio = str(n) + ') ' + r.fik
            if r.fik != usna:
                col = str(n % 3)
            else:
                col = '3'
            tt.append([col, fio, r.scorTD])
    data = {
        'tt': tt,
        'tx1': 'ТОП сегодняшнего дня',
        'tx2': 'Текущие достижения текущего дня',
        'tx3': 'В таблице отображается Ваш лучший сегодняшний результат'
    }
    return render(request, 'jsprob/topday.html', data)


def topglob(request):
    dayend()
    tt = []
    try:
        usna = request.user.first_name.replace('$#$%', ' ')
    except:
        usna = ''
    n = 0
    for r in DataUser.objects.order_by('-res1'):
        if r.scores != 0:
            n += 1
            fio = str(n) + ') ' + r.fik
            if r.fik != usna:
                col = str(n % 3)
            else:
                col = '3'
            tt.append([col, fio, r.res1])
    data = {
        'tt': tt,
        'tx1': 'Глобальный ТОП',
        'tx2': 'Достижения всех игроков за все время',
        'tx3': 'В таблице отображаются лучшие результаты'
    }
    return render(request, 'jsprob/topday.html', data)


def reset(request):
    if (request.user.is_superuser) != True: return redirect('home')
    if request.method == 'GET':
        answer = request.GET
        if 'res' in answer:
            allpolz = DataUser.objects.all()
            for allp in allpolz:
                if allp.pole2.count('$') != 7:
                    allp.pole2 = '0$1$0$0$0$0$0$0'
                p2 = allp.pole2.split('$')
                po = '1'
                if float(p2[3]) + float(p2[4]) + float(p2[5]) + float(p2[6]) + float(p2[7]) > 0: po = '2'
                allp.pole2 = '0$' + po + '$0$' + p2[3] + '$' + p2[4] + '$' + p2[5] + '$' + p2[6] + '$' + p2[7]
                allp.scores = 0
                allp.save()
            allpolz = TopTabllev.objects.all()
            i = 0
            for allp in allpolz:
                i += 1
                if i > 1:
                    allp.fio = 'Иванов Николай 11Б$^%^Петрова Нина Константиновна$^%^Буренко Алексей Сергеевич$^%^Сидоров Илья 10$^%^Мельников Григорий 8$^%^Светлоусов Женя 6$^%^Муртазина Оля 4$^%^B$^%^F'
                    allp.scor = '10000_8000_6000_4000_3000_2000_1000_500_300'
                    allp.save()
            return redirect('home')
    return render(request, 'jsprob/reset.html')


def begin(request):
    dayend()
    usna = request.user.username
    # ud = request.COOKIES.get('keyshif').split('$')
    # print('ud=', ud)
    tt = DataUser.objects.get(log=usna)
    popmas = tt.pole1.split(
        '$')  # pole1 = Попыток в сезоне $ Пройдено игр в сезоне $ Попыток всего  pop - попыток всего
    popmas[0] = str(int(float(popmas[0]) + 1))
    popmas[2] = str(int(float(popmas[2]) + 1))
    DataUser.objects.filter(log=usna).update(pole1='$'.join(popmas))
    request.session['ustns4usen'] = usna
    usefio = request.user.first_name.split('$#$%')
    request.session['ustns4usennam'] = usefio[1]
    return render(request, 'jsprob/level1.html',
                  {'usp': 'Успеха, ' + usefio[1], 'lv': 'Этап 1.', 'namlv': 'Разминка', 'list': 'list1'})


# def level2(request):
#     ud = request.COOKIES.get('lelrec15').split('$')
#     usefio = request.user.first_name.split('$#$%')
#     if ud[0] != 'e':
#         if float(ud[0]) < float(ud[1]):
#             DataUser.objects.filter(log=request.session['ustns4usen']).update(scoresl1=ud[1])
#     return render(request, 'jsprob/level2.html', {'nm': usefio[1]})
#
#
# def level3(request):
#     ud = request.COOKIES.get('lelrec15').split('$')
#     if ud[0] != 'e':
#         if float(ud[0]) < float(ud[1]):
#             DataUser.objects.filter(log=request.session['ustns4usen']).update(scoresl2=ud[1])
#     return render(request, 'jsprob/level3.html')
#
#
# def level4(request):
#     ud = request.COOKIES.get('lelrec15').split('$')
#     if ud[0] != 'e':
#         if float(ud[0]) < float(ud[1]):
#             DataUser.objects.filter(log=request.session['ustns4usen']).update(scoresl3=ud[1])
#     return render(request, 'jsprob/level4.html')
#
#
# def level5(request):
#     ud = request.COOKIES.get('lelrec15').split('$')
#     if ud[0] != 'e':
#         if float(ud[0]) < float(ud[1]):
#             DataUser.objects.filter(log=request.session['ustns4usen']).update(scoresl4=ud[1])
#     return render(request, 'jsprob/level5.html')


def list1(request):
    Vyb = Vyborka(0, 10)
    data = {'ti': 4000, 'tas1': Vyb.t1, 'tas2': Vyb.t2, 'tasz': Vyb.tz, 'otv': Vyb.ot}
    return render(request, 'jsprob/list1.html', data)


def list2(request):
    Vyb = Vyborka(10, 20)
    return render(request, 'jsprob/list2.html',
                  {'tas1': Vyb.t1, 'tas2': Vyb.t2, 'tasz': Vyb.tz, 'otv': Vyb.ot, 'ti': 7000})


def list3(request):
    Vyb = Vyborka(20, 30)
    return render(request, 'jsprob/list3.html',
                  {'tas1': Vyb.t1, 'tas2': Vyb.t2, 'tasz': Vyb.tz, 'otv': Vyb.ot, 'ti': 8000})


def list4(request):
    Vyb = Vyborka(30, 40)
    return render(request, 'jsprob/list4.html',
                  {'tas1': Vyb.t1, 'tas2': Vyb.t2, 'tasz': Vyb.tz, 'otv': Vyb.ot, 'ti': 10000})


def list5(request):
    Vyb = Vyborka(40, 50)
    return render(request, 'jsprob/list5.html',
                  {'tas1': Vyb.t1, 'tas2': Vyb.t2, 'tasz': Vyb.tz, 'otv': Vyb.ot, 'ti': 9000})


def itoglv(request):
    ud = request.COOKIES.get('lelrec15').split('$')
    if ud[0] == 'e': return redirect('home')
    lastlv = int(float(ud[0]))
    usna = request.session['ustns4usen']
    us = DataUser.objects.get(log=usna)
    krit = 'scoresl' + str(ud[0])
    sclvus = DataUser.objects.filter(log=usna, fik=us.fik).values_list(krit)[0][
        0]  # с каждым этапом меняем поле, к которому обращаемся, поэтому так заморочено
    mn = sclvus
    tx = orf1(mn) + '.'
    # if (mn // 10) % 10 != 1:
    #     if mn % 10 == 2 or mn % 10 == 3 or mn % 10 == 4: tx = ' очка.'
    #     if mn % 10 == 1: tx = ' очко.'
    vstsl = ['На разминке ', 'Во втором ', 'В третьем ', 'В четвертом ', 'В пятом ', 'В шестом '][lastlv - 1]
    txt1 = vstsl + 'этапе Вы набрали ' + ud[1] + tx
    txt2 = 'Решено правильно: ' + ud[2] + '; из них безошибочно: ' + ud[3] + '. '
    txt5 = ''
    txtpz = ''
    txt6 = ''

    if float(ud[1]) > float(sclvus):
        txt5 = 'Вы улучшили собственный рекорд пройденного этапа на ' + str(int(float(ud[1]) - float(sclvus))) + '. ' \
               + ' (' + str(int(float(sclvus))) + ' --> ' + str(int(float(ud[1]))) + ')'

        mas0 = [i for i in DataUser.objects.filter(scoresl1__gt=sclvus).order_by('-' + krit).values_list(krit, 'fik')]
        if ud[0] == '1':
            mas0 = [i for i in
                    DataUser.objects.filter(scoresl1__gt=sclvus).order_by('-' + krit).values_list(krit, 'fik')]
            DataUser.objects.filter(log=usna).update(scoresl1=ud[1])
            mas1 = [i for i in
                    DataUser.objects.filter(scoresl1__gt=ud[1]).order_by('-' + krit).values_list(krit, 'fik')]
        if ud[0] == '2':
            mas0 = [i for i in
                    DataUser.objects.filter(scoresl2__gt=sclvus).order_by('-' + krit).values_list(krit, 'fik')]
            DataUser.objects.filter(log=usna).update(scoresl2=ud[1])
            mas1 = [i for i in
                    DataUser.objects.filter(scoresl2__gt=ud[1]).order_by('-' + krit).values_list(krit, 'fik')]
        if ud[0] == '3':
            mas0 = [i for i in
                    DataUser.objects.filter(scoresl3__gt=sclvus).order_by('-' + krit).values_list(krit, 'fik')]
            DataUser.objects.filter(log=usna).update(scoresl3=ud[1])
            mas1 = [i for i in
                    DataUser.objects.filter(scoresl3__gt=ud[1]).order_by('-' + krit).values_list(krit, 'fik')]
        if ud[0] == '4':
            mas0 = [i for i in
                    DataUser.objects.filter(scoresl4__gt=sclvus).order_by('-' + krit).values_list(krit, 'fik')]
            DataUser.objects.filter(log=usna).update(scoresl4=ud[1])
            mas1 = [i for i in
                    DataUser.objects.filter(scoresl4__gt=ud[1]).order_by('-' + krit).values_list(krit, 'fik')]
        if ud[0] == '5':
            mas0 = [i for i in
                    DataUser.objects.filter(scoresl5__gt=sclvus).order_by('-' + krit).values_list(krit, 'fik')]
            DataUser.objects.filter(log=usna).update(scoresl5=ud[1])
            mas1 = [i for i in
                    DataUser.objects.filter(scoresl5__gt=ud[1]).order_by('-' + krit).values_list(krit, 'fik')]
        if ud[0] == '6':
            mas0 = [i for i in
                    DataUser.objects.filter(scoresl6__gt=sclvus).order_by('-' + krit).values_list(krit, 'fik')]
            DataUser.objects.filter(log=usna).update(scoresl6=ud[1])
            mas1 = [i for i in
                    DataUser.objects.filter(scoresl6__gt=ud[1]).order_by('-' + krit).values_list(krit, 'fik')]
        pos_old = int(len(mas0) + 1)
        pos_now = int(len(mas1) + 1)
        if pos_now < 11:
            if pos_old == pos_now:
                txtpz = 'Поздравляем!'
                if pos_now != 1:
                    txt6 = 'Вы еще прочнее укрепились на ' + str(pos_now) + '-позиции в TOP-10 пройденного уровня.'
                else:
                    txt6 = 'Вы еще сильнее утвердили свое ЛИДЕРСТВО в пройденном этапе.'
            else:
                if pos_old > 10:
                    if pos_now != 1:
                        txtpz = 'ПОЗДРАВЛЯЕМ!'
                        txt6 = 'На данный момент Вы вошли в TOП-10 пройденного уровня! \
                                 ( ' + str(pos_now) + ' место )'
                    else:
                        txtpz = 'ПОЗДРАВЛЯЕМ!!!'
                        txt6 = 'На данный момент Вы врываетесь в ТОП-10 и становитесь ЧЕМПИОНОМ пройденного уровня.'
                else:
                    if pos_now != 1:
                        txtpz = 'ПОЗДРАВЛЯЕМ!'
                        txt6 = 'Вы улучшили свою позицию в TOП-10 пройденного этапа. ( ' + \
                               str(pos_old) + ' --> ' + str(pos_now) + ' )'
                    else:
                        txtpz = 'ПОЗДРАВЛЯЕМ!!!'
                        txt6 = 'На данный момент Вы становитесь ЧЕМПИОНОМ пройденного уровня!'
        else:
            if pos_old != pos_now:
                txt6 = 'В TOП-е пройденного этапа Ваше место стало выше. ( ' + \
                       str(pos_old) + ' --> ' + str(pos_now) + ' )'
    else:
        if float(ud[1]) < float(sclvus) * .8:
            txt6 = 'Соберитесь. Ваш личный рекорд пройденного этапа куда выше.'
        if float(ud[1]) > float(sclvus) * .97 and float(ud[1]) != float(sclvus):
            txt6 = 'Еще немного и Ваш рекорд пройденного этапа ( ' + str(int(float(sclvus))) + ' ) был бы побит.'

        # print('sclvus:', sclvus, '  ud[1]:', ud[1])
        #
        # print('mas0:', mas0, len(mas0), '   mas1:', mas1, len(mas1))

    if request.method == 'GET':
        answer = request.GET
        if 'prod' in answer:
            if ud[0] == '5':  # '5' - количество этапов
                DataUser.objects.filter(log=usna).update(pole2='0')
                return redirect('itog')
            meslv = 'Этап ' + str(int(float(ud[0]) + 1)) + '.'
            mesnam = ['"Сквозь десятки"', "Минуя сотни", '"Хитрое" умножение', '"Life hack"-Деление', 'Назв 6.'][
                lastlv - 1]
            usp = ['Удачи, ' + request.session['ustns4usennam'] + '!', '', '', '', '', ''][lastlv - 1]
            return render(request, 'jsprob/level1.html',
                          {'usp': usp, 'lv': meslv, 'namlv': mesnam, 'list': 'list' + str(lastlv + 1)})
    return render(request, 'jsprob/itoglv.html',
                  {'txt1': txt1, 'txt2': txt2, 'txt5': txt5, 'txt6': txt6, 'txtpz': txtpz})


class Examples:
    def __init__(self, rab, mm):
        otvs = [[''] * 1 for i in range(60)]  # №задачи (кол-во вариантов -1), количество задач (№ коретжа)
        tasks = [[''] * 1 for i in range(60)]  # №задачи (кол-во вариантов -1), количество задач (№ коретжа)

        for r in range(0, rab):
            # Устный счет
            # сложение
            if mm == 0:
                provsov = [[0] * 3 for i in range(11)]  # обнуление массива контроля повторений
                for z in range(0, 5):
                    while True:
                        fl = 0
                        a = randint(2, 8)
                        b = randint(1, 10 - a)
                        mas = provsov
                        for d in range(0, 5):  # все 5 используя предыдущие
                            if (mas[d][0] == a) and (mas[d][1] == b) or (mas[d][0] == b) and (mas[d][1] == a) \
                                    or (mas[d][2] == a + b):
                                fl = 1
                        if fl == 0:
                            provsov[z][0] = a
                            provsov[z][1] = b
                            provsov[z][2] = a + b
                            tasks[z][r] = str(a) + '+' + str(b) + '='
                            otvs[z][r] = '0'  # otvs[y + z][r] = str(a + b)
                            break

                # вычитание
                provsov = [[0] * 3 for i in range(11)]
                for z in range(5, 10):
                    while True:
                        fl = 0
                        b = randint(1, 8)
                        a = randint(b + 1, 9)
                        mas = provsov
                        for d in range(0, 5):  # все 5 используя предыдущие
                            if (mas[d][0] == a) and (mas[d][1] == b) or (mas[d][0] == b) and (mas[d][1] == a) or (
                                    mas[d][2] == a - b):
                                fl = 1
                        if fl == 0:
                            provsov[z - 5][0] = a
                            provsov[z - 5][1] = b
                            provsov[z - 5][2] = a - b
                            tasks[z][r] = str(a) + '–' + str(b) + '='
                            otvs[z][r] = '0'  # otvs[y + z][r] = str(a - b)
                            break

            if mm == 10:
                # сложение через десяток
                provsov = [[0] * 3 for i in range(11)]
                for z in range(10, 15):
                    while True:
                        fl = 0
                        while True:
                            a = randint(2, 9)
                            b = randint(10 - a, 9)
                            if (a + b) % 10 >= int(1.5 * (z - 10)) and (a + b) != 11:
                                break
                        mas = provsov
                        for d in range(0, 5):  # все 5 используя предыдущие
                            if (mas[d][0] == a) and (mas[d][1] == b) or (mas[d][0] == b) and (mas[d][1] == a) or (
                                    mas[d][2] == a + b):
                                fl = 1
                        if fl == 0:
                            provsov[z - 10][0] = a
                            provsov[z - 10][1] = b
                            provsov[z - 10][2] = a + b
                            while True:
                                fl0 = 0
                                if (randint(0, 1) == 0):
                                    a = a + 10 * randint((z - 10), (z - 10) * 2)
                                else:
                                    b = b + 10 * randint((z - 10), (z - 10) * 2)
                                prst = str(a + b)
                                for d in range(0, 10):
                                    if prst.find(str(d) + str(d)) != -1:
                                        a = a % 10
                                        b = b % 10
                                        fl0 = 1
                                if fl0 == 0: break
                            tasks[z][r] = str(a) + '+' + str(b) + '='
                            otvs[z][r] = str(a + b)
                            break
                lg = 11
                pg = 14
                rb = r
                k = randint(20, 25)
                for z in range(1, k):
                    while True:
                        i = randint(lg, pg)
                        ii = randint(lg, pg)
                        if (i != ii):
                            break
                    tasks[i][rb], tasks[ii][rb] = tasks[ii][rb], tasks[i][rb]
                    otvs[i][rb], otvs[ii][rb] = otvs[ii][rb], otvs[i][rb]

                # вычитание через десяток
                provsov = [[0] * 2 for i in range(11)]
                for z in range(15, 20):
                    while True:
                        fl = 0
                        while True:
                            a = randint(2, 9)
                            b = randint(10 - a, 9)
                            if (a + b) % 10 >= int(1.5 * (z - 15)):
                                break
                        mas = provsov
                        for d in range(0, 5):  # все 5 используя предыдущие
                            if (mas[d][0] == a) and (mas[d][1] == b) or (mas[d][0] == b) and (mas[d][1] == a):
                                fl = 1
                        if fl == 0:
                            provsov[z - 15][0] = a
                            provsov[z - 15][1] = b
                            while True:
                                fl0 = 0
                                i = randint(0, 1)
                                if (i == 0):
                                    a = a + 10 * randint((z - 15), (z - 15) * 2)
                                else:
                                    b = b + 10 * randint((z - 15), (z - 15) * 2)
                                for d in range(0, 10):
                                    if i == 0:
                                        if str(a).find(str(d) + str(d)) != -1:
                                            a = a % 10
                                            b = b % 10
                                            fl0 = 1
                                    if i == 1:
                                        if str(b).find(str(d) + str(d)) != -1:
                                            a = a % 10
                                            b = b % 10
                                            fl0 = 1
                                if fl0 == 0: break
                            if (i == 0):
                                tasks[z][r] = str(a + b) + '–' + str(b) + '='
                                otvs[z][r] = str(a)
                            else:
                                tasks[z][r] = str(a + b) + '–' + str(a) + '='
                                otvs[z][r] = str(b)
                            break

            if mm == 20:
                # сложение через сотню
                provsov = [[0] * 3 for i in range(11)]
                for z in range(20, 25):
                    while True:
                        fl = 0
                        while True:
                            a = randint(5, 9)
                            b = randint(10 - a, 9)
                            if (a + b) % 10 >= int(1.5 * (z - 20)) and ((a + b) % 10 != 0):
                                break
                        i = randint(int((z - 18) * 0.7), z - 19) * 100
                        a = 100 - 10 * (randint(int((z - 20) * 0.35), int((z - 20) * 0.6)) + 1) + a
                        b = randint(int((z - 19) * 0.5), int((z - 19) * 0.9)) * 10 + b  # 45-1
                        prst = str(a + i - 100 + b)
                        for d in range(0, 10):
                            if prst.find(str(d) + str(d)) != -1: fl = -1
                        mas = provsov
                        for d in range(0, 5):  # все 5 используя предыдущие
                            if (mas[d][0] == a) or (mas[d][1] == b) or (mas[d][0] == b) or (mas[d][1] == a) or (
                                    mas[d][2] == a + b):
                                fl = 1
                        if fl == 0:
                            provsov[z - 20][0] = a
                            provsov[z - 20][1] = b
                            provsov[z - 20][2] = a + b
                            a = a + i - 100
                            if (randint(0, 1) == 0):
                                tasks[z][r] = str(a) + '+' + str(b) + '='
                            else:
                                tasks[z][r] = str(b) + '+' + str(a) + '='
                            otvs[z][r] = str(a + b)
                            break

                # вычитание через сотню
                provsov = [[0] * 2 for i in range(11)]
                for z in range(25, 30):
                    while True:
                        fl = 0
                        while True:
                            a = randint(5, 9)
                            b = randint(10 - a, 9)
                            if ((a + b) % 10 >= int(1.5 * (z - 25))) and ((a + b) % 10 != 0):
                                break
                        i = randint(int((z - 23) * 0.7), z - 24) * 100
                        a = 100 - 10 * (randint(int((z - 25) * 0.35), int((z - 25) * 0.6)) + 1) + a
                        b = randint(int((z - 24) * 0.5), int((z - 24) * 0.9)) * 10 + b  # 45-1
                        prst = str(b)
                        for d in range(0, 10):
                            if prst.find(str(d) + str(d)) != -1: fl = -1
                        mas = provsov
                        for d in range(0, 5):  # все 5 используя предыдущие
                            if (mas[d][0] == a) or (mas[d][1] == b) or (mas[d][0] == b) or (mas[d][1] == a):
                                fl = 1
                        if fl == 0:
                            provsov[z - 25][0] = a
                            provsov[z - 25][1] = b
                            a = a + i - 100
                            tasks[z][r] = str(a + b) + '–' + str(a) + '='
                            otvs[z][r] = str(b)
                            break

            if mm == 30:
                # умножение на 10n
                provsov = [[0] * 2 for i in range(11)]
                for z in range(30, 35):
                    while True:
                        fl = 0
                        a = randint(1, 9)
                        a = 100 + a + 100 * randint(int((z - 30) * 0.4), int((z - 30) * 0.8))
                        b = randint(2, 9)
                        prst = str(a * b)
                        for d in range(0, 10):
                            if prst.find(str(d) + str(d)) != -1: fl = -1
                        mas = provsov
                        for d in range(0, 5):  # все 5 используя предыдущие
                            if (mas[d][0] == a) or (mas[d][1] == b) or (mas[d][0] == b) or (mas[d][1] == a):
                                fl = 1
                        if fl == 0:
                            provsov[z - 30][0] = a
                            provsov[z - 30][1] = b
                            if (randint(0, 1) == 0):
                                tasks[z][r] = str(a) + '•' + str(b) + '='
                            else:
                                tasks[z][r] = str(b) + '•' + str(a) + '='
                            otvs[z][r] = str(a * b)
                            break

                # умножение на 100-n
                provsov = [[0] * 2 for i in range(11)]
                for z in range(35, 40):
                    while True:
                        fl = 0
                        a = randint(1, 4)
                        a = 100 + 100 * randint(int((z - 35) * 0.4), int((z - 35) * 0.8)) - a
                        b = randint(2, 9)
                        prst = str(a * b)
                        for d in range(0, 10):
                            if prst.find(str(d) + str(d)) != -1: fl = -1
                        mas = provsov
                        for d in range(0, 5):  # все 5 используя предыдущие
                            if (mas[d][0] == a) or (mas[d][1] == b) or (mas[d][0] == b) or (mas[d][1] == a):
                                fl = 1
                        if fl == 0:
                            provsov[z - 35][0] = a
                            provsov[z - 35][1] = b
                            if (randint(0, 1) == 0):
                                tasks[z][r] = str(a) + '•' + str(b) + '='
                            else:
                                tasks[z][r] = str(b) + '•' + str(a) + '='
                            otvs[z][r] = str(a * b)
                            break

            if mm == 40:
                # деление числа 10n*k/k
                provsov = [[0] * 2 for i in range(11)]
                for z in range(40, 45):
                    while True:
                        fl = 0
                        a = randint(1, 9)
                        a = 100 + a + 100 * randint(int((z - 40) * 0.4), int((z - 40) * 0.8))
                        b = randint(2, 9)
                        prst = str(a)
                        for d in range(0, 10):
                            if prst.find(str(d) + str(d)) != -1: fl = -1
                        mas = provsov
                        for d in range(0, 5):  # все 5 используя предыдущие
                            if (mas[d][0] == a) or (mas[d][1] == b) or (mas[d][0] == b) or (mas[d][1] == a):
                                fl = 1
                        if fl == 0:
                            provsov[z - 40][0] = a
                            provsov[z - 40][1] = b
                            tasks[z][r] = str(a * b) + ':' + str(b) + '='
                            otvs[z][r] = str(a)
                            break

                # деление числа (100-n)*k/k
                provsov = [[0] * 2 for i in range(11)]
                for z in range(45, 50):
                    while True:
                        fl = 0
                        a = randint(1, 5)
                        a = 100 - a + 100 * randint(int((z - 45) * 0.4), int((z - 45) * 0.8))
                        b = randint(2, 9)
                        prst = str(a)
                        for d in range(0, 10):
                            if prst.find(str(d) + str(d)) != -1: fl = -1
                        mas = provsov
                        for d in range(0, 5):  # все 5 используя предыдущие
                            if (mas[d][0] == a) or (mas[d][1] == b) or (mas[d][0] == b) or (mas[d][1] == a):
                                fl = 1
                        if fl == 0:
                            provsov[z - 45][0] = a
                            provsov[z - 45][1] = b
                            tasks[z][r] = str(a * b) + ':' + str(b) + '='
                            otvs[z][r] = str(a)
                            break

            if mm == 50:
                # разность квадратов
                a = randint(112, 149)
                tasks[50][r] = str(a) + '²–' + str(a - 100) + '²='
                otvs[50][r] = str(((a - 100) * 2 + 100) * 100)
                # разность квадратов через симметричные множители
                a = randint(2, 9) * 10
                b = randint(1, 3)
                while True:
                    c = randint(2, 9) * 10
                    if a != c: break
                d = randint(4,7)
                if randint(0, 1) == 0:
                    tasks[51][r] = str(a - b) + '•' + str(a + b) + '='
                else:
                    tasks[51][r] = str(a + b) + '•' + str(a - b) + '='
                otvs[51][r] = str(a * a - b * b)
                if randint(0, 1) == 0:
                    tasks[52][r] = str(c - d) + '•' + str(c + d) + '='
                else:
                    tasks[52][r] = str(c + d) + '•' + str(c - d) + '='
                otvs[52][r] = str(c * c - d * d)

                # 6 разнознаковых
                s = [0 for i in range(3)]
                r = [0 for i in range(3)]
                while True:
                    for d in range(3):
                        q = gene(d+2)
                        r[d] = q[0]
                        s[d] = q[1]
                    if sum([p / abs(p) for p in s if p > 0]) == 1 \
                            and abs(s[0]) != abs(s[1]) and abs(s[0]) != abs(s[2]) and abs(s[1]) != abs(s[2]):
                        break
                st = ['' for i in range(3)]
                for n in range(3):
                    for m in r[n]:
                        if m > 0 and m != r[n][0]:
                            st[n] = st[n] + '+' + str(m)
                        else:
                            st[n] = st[n] + str(m)




                    fl = 0
                    a = randint(1, 9)
                    a = 100 + a + 100 * randint(int((z - 40) * 0.4), int((z - 40) * 0.8))
                    b = randint(2, 9)
                    prst = str(a)
                    for d in range(0, 10):
                        if prst.find(str(d) + str(d)) != -1: fl = -1
                    mas = provsov
                    for d in range(0, 5):  # все 5 используя предыдущие
                        if (mas[d][0] == a) or (mas[d][1] == b) or (mas[d][0] == b) or (mas[d][1] == a):
                            fl = 1
                    if fl == 0:
                        provsov[z - 40][0] = a
                        provsov[z - 40][1] = b
                        tasks[z][r] = str(a * b) + ':' + str(b) + '='
                        otvs[z][r] = str(a)
                        break

                # деление числа (100-n)*k/k
                provsov = [[0] * 2 for i in range(11)]
                for z in range(45, 50):
                    while True:
                        fl = 0
                        a = randint(1, 5)
                        a = 100 - a + 100 * randint(int((z - 45) * 0.4), int((z - 45) * 0.8))
                        b = randint(2, 9)
                        prst = str(a)
                        for d in range(0, 10):
                            if prst.find(str(d) + str(d)) != -1: fl = -1
                        mas = provsov
                        for d in range(0, 5):  # все 5 используя предыдущие
                            if (mas[d][0] == a) or (mas[d][1] == b) or (mas[d][0] == b) or (mas[d][1] == a):
                                fl = 1
                        if fl == 0:
                            provsov[z - 45][0] = a
                            provsov[z - 45][1] = b
                            tasks[z][r] = str(a * b) + ':' + str(b) + '='
                            otvs[z][r] = str(a)
                            break

        self.tas = tasks
        self.ot = otvs


def gene(pol):
    while True:
        s = []
        for i in range(6):
            while True:
                k = randint(1, 9) * (2 * randint(0, 1) - 1)
                if k not in s and -k not in s:
                    s.append(k)
                    break
        su = sum([p for p in s])
        if sum([p / abs(p) for p in s if p > 0]) == pol and su != 0:
            break
    return s, su


class Vyborka:
    def __init__(self, m, n):
        rab = 1
        Ex = Examples(rab, m)
        tasks = []
        for i in range(len(Ex.tas)): tasks.append(Ex.tas[i][0])
        simv = ['+', '–', '•', ':']
        tasks1 = []
        tasksz = []
        tasks2 = []
        otvs = randint(12, 98)
        for r in range(m, n):
            for z in range(4):
                if tasks[r].find(simv[z]) != -1:
                    x = tasks[r].find(simv[z])
                    tasks1.append(float(tasks[r][:x]) + otvs + (r - m) ** 2)
                    tasksz.append(z)
                    tasks2.append(float(tasks[r][x + 1:len(tasks[r]) - 1]))

        self.t1 = tasks1
        self.t2 = tasks2
        self.tz = tasksz
        self.ot = otvs


class Defuser:
    def __init__(self, fio, lv, usna):
        krit = 'scoresl' + str(lv)
        mas = [i for i in DataUser.objects.order_by('-' + krit).values_list(krit, 'fik')][:10]
        sclvus = DataUser.objects.filter(log=usna, fik=fio).values_list(krit)[0][0]
        print('sclvus', sclvus)
        # mas = [i for i in DataUser.objects.filter(scores__gt=84000).order_by(krit).values_list('scoresl1')]
        sctop = [i[0] for i in mas]
        fiktop = [i[1] for i in mas]
        if fio in fiktop:
            fl0 = 1
            scnow = sclvus
        else:
            fl0 = 0
            scnow = 0  # сколько очков у игрока в ТОП-е

        self.minsc = sctop[9]
        self.fl00 = fl0
        self.scnow = scnow
        self.sclvus = sclvus


class Upuserez:
    def __init__(self, fio, lv, re, usna):
        tabsc = DataUser.objects.get(pole1=fio, log=usna)
        sclvus = tabsc.pole2.split('$')
        p2 = ''
        i = 0
        for sc in sclvus:
            i += 1
            if i == (lv + 3):
                p2 = p2 + re + '$'
            else:
                p2 = p2 + sc + '$'
        p2 = p2[:(len(p2) - 1)]
        tabsc.pole2 = p2
        tabsc.save(update_fields=['pole2'])


class Inttabl:
    def __init__(self, fio, lv, re):
        tablv = Indexs.objects.get(log=lv)
        sctablv = tablv.scor.split('_')
        ustablv = tablv.fio.split('$^%^')
        if fio not in ustablv:
            sctablv.append(re)
            ustablv.append(fio)
        i = 1
        while i == 1:
            i = 0
            for z in range(1, len(sctablv)):
                if float(sctablv[z - 1]) < float(sctablv[z]):
                    sctablv[z - 1], sctablv[z] = sctablv[z], sctablv[z - 1]
                    ustablv[z - 1], ustablv[z] = ustablv[z], ustablv[z - 1]
                    i = 1
        p2 = ''
        p1 = ''
        for i in range(9):
            if i != 8:
                p1 = p1 + sctablv[i] + '_'
                p2 = p2 + ustablv[i] + '$^%^'
            else:
                p1 = p1 + sctablv[i]
                p2 = p2 + ustablv[i]
        tablv.fio = p2
        tablv.scor = p1
        tablv.save()


class UpInttabl:
    def __init__(self, fio, lv, re):
        tablv = Indexs.objects.get(log=lv)
        sctablv = tablv.scor.split('_')
        ustablv = tablv.fio.split('$^%^')
        if fio in ustablv:
            sctablv[ustablv.index(fio)] = re
            i = 1
            while i == 1:
                i = 0
                for z in range(1, len(sctablv)):
                    if float(sctablv[z - 1]) < float(sctablv[z]):
                        sctablv[z - 1], sctablv[z] = sctablv[z], sctablv[z - 1]
                        ustablv[z - 1], ustablv[z] = ustablv[z], ustablv[z - 1]
                        i = 1
            p2 = ''
            p1 = ''
            for i in range(9):
                if i != 8:
                    p1 = p1 + sctablv[i] + '_'
                    p2 = p2 + ustablv[i] + '$^%^'
                else:
                    p1 = p1 + sctablv[i]
                    p2 = p2 + ustablv[i]
            tablv.fio = p2
            tablv.scor = p1
            tablv.save()
        else:
            Inttabl(fio, lv, re)


def instr(request):
    return render(request, 'jsprob/instr.html')


class Prit4i:
    def __init__(self):
        mp = ['«Скажи мудрости: «Ты сестра моя!» и разум назови родным твоим.» Притчи Соломона 7:4',
              '«Скудоумный высказывает презрение к ближнему своему; но разумный человек молчит.» Притчи Соломона 11:12',
              '«Добрый разум доставляет приятность, путь же беззаконных жесток.» Притчи Соломона 13:15',
              '«Всякий благоразумный действует с знанием, а глупый выставляет напоказ глупость.» Притчи Соломона 13:17',
              '«Ухо, внимательное к учению жизни, пребывает между мудрыми.» Притчи Соломона 15:31',
              '«Приобретение мудрости гораздо лучше золота, и приобретение разума предпочтительнее отборного серебра.» Притчи Соломона 16:16',
              '«На разумного сильнее действует выговор, нежели на глупого сто ударов.» Притчи Соломона 17:10',
              '«Лучше встретить человеку медведицу, лишенную детей, нежели глупца с его глупостью.» Притчи Соломона 17:12',
              '«И глупец, когда молчит, может показаться мудрым, и затворяющий уста свои – благоразумным.» Притчи Соломона 17:28',
              '«Сердце разумного приобретает знание, и ухо мудрых ищет знания.» Притчи Соломона 18:16',
              '«Нехорошо душе без знания, и торопливый ногами оступится.» Притчи Соломона 19:2',
              '«Кто приобретает разум, тот любит душу свою; кто наблюдает благоразумие, тот находит благо.» Притчи Соломона 19:8',
              '«Главное — мудрость: приобретай мудрость, и всем имением твоим приобретай разум.» Притчи Соломона 4:7',
              '«Невежды получают себе в удел глупость, а благоразумные увенчаются знанием» Притчи Соломона 14:18',
              '«От всякого труда есть прибыль, а от пустословия только ущерб» Притчи Соломона 14:27',
              '«У терпеливого человека много разума, а раздражительный выказывает глупость» Притчи Соломона 14:29',
              '«Благоразумный видит беду и укрывается; а неопытные идут вперед и наказываются» Притчи Соломона 27:12',
              '«Подарок тайный тушит гнев, и дар в пазуху — сильную ярость.» Притчи Соломона 21:14',
              '«Помыслы в сердце человека – глубокие воды, но человек разумный вычерпывает их.» Притчи Соломона 20:5',
              '«Кто хранит наставление, тот на пути к жизни; а отвергающий обличение – блуждает.» Притчи Соломона 10:17',
              '«Мерзость перед Господом всякий надменный сердцем; можно поручиться, что он не останется ненаказанным.» Притчи Соломона 16:5',
              '«Когда мудрость войдет в сердце твое, и знание будет приятно душе твоей, тогда рассудительность будет оберегать тебя, разум будет охранять тебя.» Притчи Соломона 2:10-11',
              '«Посему ходи путем добрых и держись стезей праведников.» Притчи Соломона 2:20',
              '«Милость и истина да не оставляют тебя: обвяжи ими шею твою, напиши их на скрижали сердца твоего, и обретешь благоволение в очах Бога и людей.» Притчи Соломона 3:3-4',
              '«Блажен человек, который снискал мудрость, и человек, который приобрел разум,...» Притчи Соломона 3:13',
              '«Не отказывай в благодеянии нуждающемуся, когда рука твоя в силе сделать его.» Притчи Соломона 3:27',
              '«Не замышляй против ближнего твоего зла, когда он без опасения живет с тобою.» Притчи Соломона 3:29',
              '«Мудрые наследуют славу, а глупые — бесславие.» Притчи Соломона 3:35',
              '«потому что мудрость лучше жемчуга, и ничто из желаемого не сравнится с нею.» Притчи Соломона 8:11',
              '«Я - Мудрость, обитаю с Благоразумием. Я — Знание, меня можно найти в предосторожности.» Притчи Соломона 8:12',
              '«оставьте неразумие, и живите, и ходите путем разума.» Притчи Соломона 9:6',
              '«Ненависть возбуждает раздоры, но любовь покрывает все грехи.» Притчи Соломона 10:12',
              '«В устах разумного находится мудрость, но на теле глупого - розга.» Притчи Соломона 10:13',
              '«Мудрые сберегают знание, но уста глупого — близкая погибель.» Притчи Соломона 10:14',
              '«При многословии не миновать греха, а сдерживающий уста свои — разумен.» Притчи Соломона 10:19',
              '«Уста праведного пасут многих, а глупые умирают от недостатка разума.» Притчи Соломона 10:21',
              '«Для глупого преступное деяние как бы забава, а человеку разумному свойственна мудрость.» Притчи Соломона 10:23',
              '«Чего страшится нечестивый, то и постигнет его, а желание праведников исполнится.» Притчи Соломона 10:24',
              '«Что уксус для зубов и дым для глаз, то ленивый для посылающих его.» Притчи Соломона 10:26',
              '«Придет гордость, придет и посрамление; но со смиренными — мудрость.» Притчи Соломона 11:2',
              '«Честность управляет поступками праведных людей, но злые, обманывая других, уничтожают самих себя.» Притчи Соломона 11:3',
              '«Жизнь доброго человека будет легкой, если он честен, а злого погубит собственное зло.» Притчи Соломона 11:5',
              '«Своими устами безбожные губят ближнего, но праведные спасаются своим знанием.» Притчи Соломона 11:9',
              '«Благословением праведных возвышается город, а устами нечестивых разрушается.» Притчи Соломона 11:11',
              '«Человек милосердный благотворит душе своей, а жестокосердый разрушает плоть свою.» Притчи Соломона 11:17',
              '«Нечестивый делает дело ненадежное, а сеющему правду — награда верная.» Притчи Соломона 11:18',
              '«Что золотое кольцо в носу у свиньи, то женщина красивая и — безрассудная.» Притчи Соломона 11:22',
              '«Иной сыплет щедро, и ему еще прибавляется; а другой сверх меры бережлив, и однако же беднеет.» Притчи Соломона 11:24',
              '«Кто стремится к добру, тот ищет благоволения; а кто ищет зла, к тому оно и приходит.» Притчи Соломона 11:27',
              '«Не утвердит себя человек беззаконием; корень же праведных неподвижен.» Притчи Соломона 12:3',
              '«Хвалят человека по мере разума его, а развращенный сердцем будет в презрении.» Притчи Соломона 12:8',
              '«От плода уст своих человек насыщается добром, и воздаяние человеку — по делам рук его.» Притчи Соломона 12:14',
              '«У глупого тотчас же выкажется гнев его, а благоразумный скрывает оскорбление.» Притчи Соломона 12:16',
              '«Иной пустослов уязвляет как мечом, а язык мудрых — врачует.» Притчи Соломона 12:18',
              '«Человек рассудительный скрывает знание, а сердце глупых выказывает глупость.» Притчи Соломона 12:23',
              '«Рука прилежных будет господствовать, а ленивая будет под данью.» Притчи Соломона 12:24',
              '«Праведник указывает ближнему свой путь, а путь нечестивых вводит их в заблуждение.» Притчи Соломона 12:26',
              '«На пути правды - жизнь, и на стезе ее нет смерти.» Притчи Соломона 12:28',
              '«Кто хранит уста свои, тот бережет душу свою; а кто широко раскрывает рот, тому беда.» Притчи Соломона 13:3',
              '«Правда хранит непорочного в пути, а нечестие губит грешника.» Притчи Соломона 13:6',
              '«От высокомерия происходит раздор, а у советующихся — мудрость.» Притчи Соломона 13:10',
              '«Всякий благоразумный действует с знанием, а глупый выставляет напоказ глупость.» Притчи Соломона 13:16',
              '«Общающийся с мудрыми будет мудр, а кто дружит с глупыми, развратится.» Притчи Соломона 13:20',
              '«В устах глупого — бич гордости; уста же мудрых охраняют их.» Притчи Соломона 14:3',
              '«Распутный ищет мудрости, и не находит; а для разумного знание легко.» Притчи Соломона 14:6',
              '«Мудрость разумного — знание пути своего, глупость безрассудных — заблуждение.» Притчи Соломона 14:8',
              '«Глупые смеются над грехом, а среди праведных — благоволение.» Притчи Соломона 14:9',
              '«Дом беззаконных разорится, а жилище праведных процветет.» Притчи Соломона 14:11',
              '«Мудрый боится и удаляется от зла, а глупый раздражителен и самонадеян.» Притчи Соломона 14:16',
              '«От всякого труда есть прибыль, а от пустословия только ущерб.» Притчи Соломона 14:23',
              '«Венец мудрых — богатство их, а глупость невежд глупость и есть.» Притчи Соломона 14:24',
              '«В здоровом теле — спокойствие духа, зависть же — смертельная болезнь, проникающая до самых костей.» Притчи Соломона 14:30',
              '«Кроткий ответ отвращает гнев, а оскорбительное слово возбуждает ярость.» Притчи Соломона 15:1',
              '«Язык мудрых сообщает добрые знания, а уста глупых изрыгают глупость.» Притчи Соломона 15:2',
              '«Глупый пренебрегает наставлением отца своего; а кто внимает обличениям, тот благоразумен.» Притчи Соломона 15:5',
              '«Не любит распутный обличающих его, и к мудрым не пойдет.» Притчи Соломона 15:12',
              '«Веселое сердце делает лицо веселым, а при сердечной скорби дух унывает.» Притчи Соломона 15:13',
              '«Сердце разумного ищет знания, уста же глупых питаются глупостью.» Притчи Соломона 15:14',
              '«Лучше блюдо зелени, и при нем любовь, нежели откормленный бык, и при нем ненависть.» Притчи Соломона 15:17',
              '«Глупость — радость для малоумного, а человек разумный идет прямою дорогою.» Притчи Соломона 15:21',
              '«Без советников предприятия расстроятся, а при множестве советников они состоятся.» Притчи Соломона 15:22',
              '«Лгущий ради корысти приносит своей семье несчастья, но честного не коснутся беды.» Притчи Соломона 15:27',
              '«Ухо, внимательное к учению жизни, пребывает между мудрыми.» Притчи Соломона 15:31',
              '«Отвергающий наставление не радеет о своей душе; а кто внимает обличению, тот приобретает разум.» Притчи Соломона 15:32',
              '«Все пути человека чисты в его глазах, но Господь взвешивает души.» Притчи Соломона 16:2',
              '«Лучше немногое с правдою, нежели множество прибытков с неправдою.» Притчи Соломона 16:8',
              '«Погибели предшествует гордость, и падению — надменность.» Притчи Соломона 16:18',
              '«Лучше смиряться духом с кроткими, нежели разделять добычу с гордыми.» Притчи Соломона 16:19',
              '«Разум для имеющих его — источник жизни, а ученость глупых — глупость.» Притчи Соломона 16:22',
              '«Долготерпеливый лучше храброго, и владеющий собою лучше завоевателя города.» Притчи Соломона 16:32',
              '«Лучше кусок сухого хлеба, и с ним мир, нежели дом, полный заколотого скота с раздором.» Притчи Соломона 17:1',
              '«Неприлична глупому важная речь, тем паче знатному — уста лживые.» Притчи Соломона 17:7',
              '«Кто за зло воздает злом, от дома того не отойдет зло.» Притчи Соломона 17:13',
              '«Начало ссоры — как прорыв воды; оставь ссору прежде, нежели разгорелась она.» Притчи Соломона 17:14',
              '«Коварное сердце не найдет добра, и лукавый язык попадет в беду.» Притчи Соломона 17:20',
              '«Веселое сердце благотворно, как врачевство, а унылый дух сушит кости.» Притчи Соломона 17:22',
              '«Перед падением возносится сердце человека, а смирение предшествует славе.» Притчи Соломона 18:12',
              '«Кто дает ответ не выслушав, тот глуп, и сыд ему.» Притчи Соломона 18:13',
              '«Сердце разумного приобретает знание, и ухо мудрых ищет знания.» Притчи Соломона 18:15',
              '«Кто хочет иметь друзей, тот и сам должен быть дружелюбным; и быват друг, более привязанный, нежели брат.» Притчи Соломона 18:24',
              '«Лучше бедный, ходящий в своей непочности, нежели богатый со лживыми устами, и притом глупый.» Притчи Соломона 19:1',
              '«Лжесвидетель не останется ненаказанным, и кто говорит ложь, не спасется.» Притчи Соломона 19:5',
              '«Лень погружает в сон, а нерадивость приводит к голоду.» Притчи Соломона 19:15',
              '«Наказывай сына своего, доколе есть надежда, и не возмущайся криком его.» Притчи Соломона 19:18',
              '«Слушайся совета и принимай обличение, чтобы сделаться тебе впоследствии мудрым.» Притчи Соломона 19:20',
              '«Много замыслов в сердце человека, но состоится только определенное Господом.» Притчи Соломона 19:21',
              '«Ленивый опускает руку в чашу свою, и не хочет донести до рта своего.» Притчи Соломона 19:24',
              '«Разоряющий отца и выгоняющий мать — сын срамной и бесчестный.» Притчи Соломона 19:26',
              '«Перестань, сын мой, слушать внушения об уклонении от изречений разума.» Притчи Соломона 19:27',
              '«Честь для человека — отстать от ссоры; а всякий глупец раздорен.» Притчи Соломона 20:3',
              '«Можно узнать даже отрока по занятиям его, чисто и правильно ли будет поведение его.» Притчи Соломона 20:11',
              '«Есть золото и много жемчуга, но драгоценная утварь — уста разумные.» Притчи Соломона 20:15',
              '«Сладок для человека хлеб, приобретенный неправдою; но после рот его наполняется дресвою.» Притчи Соломона 20:17',
              '«Кто ходит переносчиком, тот открывает тайну; и кто широко раскрывает рот, с тем не сообщайся.» Притчи Соломона 20:19',
              '«Наследство, поспешно захваченное вначале, не благословится в последствии.» Притчи Соломона 20:21',
              '«Сеть для человека — поспешно давать обет, и после обета обдумывать.» Притчи Соломона 20:25',
              '«Всякий путь человека прям в глазах его; но Господь взвешивает сердца.» Притчи Соломона 21:2',
              '«Гордость очей и надменность сердца, отличающие нечстивых, — грех.» Притчи Соломона 21:4',
              '«Душа нечестивого желает зла: не найдется милости в глазах его и друг его.» Притчи Соломона 21:10',
              '«Когда наказывается кощунник, простой делается мудрым; и когда вразумляется мудрый, то он приобретает знание.» Притчи Соломона 21:11',
              '«Кто затыкает ухо от вопля бедного, тот и сам будет вопить, — и не будет услышан.» Притчи Соломона 21:13',
              '«Кто любит веселье, обеднеет; а кто любит вино и тук, не разбогатеет.» Притчи Соломона 21:17',
              '«Соблюдающий правду и милость найдет жизнь, правду и славу.» Притчи Соломона 21:21',
              '«Кто хранит уста свои и язык свой, тот хранит от бед душу свою.» Притчи Соломона 21:23',
              '«Надменный злодей — кощунник имя ему — действует в пылу гордости.» Притчи Соломона 21:24',
              '«Человек нечестивый дерзок лицом своим, а праведный держит прямо путь свой.» Притчи Соломона 21:29',
              '«Нет мудрости, и нет разума, и нет совета вопреки Господу.» Притчи Соломона 21:30',
              '«Доброе имя лучше большого богатства, и добрая слава лучше серебра и золота.» Притчи Соломона 22:1',
              '«Терны и сети на пути коварного; кто бережет душу свою, удались от них.» Притчи Соломона 22:5',
              '«Сеющий неправду пожнет беду, и трости гнева его не станет.» Притчи Соломона 22:8',
              '«Милосердный будет благословляем, потому что дает бедному от хлеба своего.» Притчи Соломона 22:9',
              '«Кто любит чистоту сердца, у того приятность на устах, тому царь — друг.» Притчи Соломона 22:11',
              '«Кто обижает бедного, чтобы умножить свое богатство, и кто дает богатому, тот обеднеет.» Притчи Соломона 22:16',
              '«Не дружись с гневливым и не сообщайся с человеком вспыльчивым, чтобы не научиться путям его и не навлечь петли на душу твою.» Притчи Соломона 22:24-25',
              '«Когда сядешь вкушать пищу с властелином, то тщательно наблюдай, что перед тобою, и поставь преграду в гортани твоей, если ты алчен.» Притчи Соломона 23:1-2',
              '«Не вкушай пищи у человека завистливого и не прельщайся лакомыми яствами его; потому что, каковы мысли в душе его, таков и он;...» Притчи Соломона 23:6-7',
              '«В уши глупого не говори, потому что он презрит разумные слова твои.» Притчи Соломона 23:9',
              '«Приложи сердце твое к учению и уши твои — к умным словам.» Притчи Соломона 23:12',
              '«Не смотри на вино, как оно краснеет, как оно ухаживается ровно: впоследствии, как змей, оно укусит, и ужалит, как аспид;» Притчи Соломона 23:31-32',
              '«Мудростью устрояется дом и разумом утверждается, и с умением внутренности его наполняются всяким драгоценным и прекрасным имуществом.» Притчи Соломона 24:3-4',
              '«Человек мудрый силен, и человек разумный укрепляет силу свою.» Притчи Соломона 24:5',
              '«Не негодуй на злодеев и не завидуй нечестивым, потому что злой не имеет будущности, — светильник нечестивых угаснет.» Притчи Соломона 24:19-20',
              '«Удали неправедного от царя, и престол его утвердится правдою.» Притчи Соломона 25:5',
              '«Не вступай поспешно в тяжбу: иначе что будешь делать при окончании, когда соперник твой осрамит тебя?» Притчи Соломона 25:8',
              '«Веди тяжбу с соперником твоим, но тайны другого не открывай, дабы не укорил тебя услышавший это, и тогда бесчестие твое не отойдет от тебя.» Притчи Соломона 25:9-10',
              '«Кротость склоняет к милости вельможа, и мягкий язык переламывает кость.» Притчи Соломона 25:15',
              '«Не учащай входить в дом друга твоего, чтобы он не наскучил тобою и не возненавидел тебя.» Притчи Соломона 25:17',
              '«Что молот и меч и острая стрела, то человек, произносящий ложное свидетельство, против ближнего своего.» Притчи Соломона 25:18',
              '«Если голоден враг твой, накорми его хлебом; и если он жаждет, напой его водою: ибо, делая сие, ты собираешь горящие угли на голову его и, Господь воздаст тебе.» Притчи Соломона 25:21-22',
              '«Как нехорошо есть много меду, так домогаться славы не есть слава.» Притчи Соломона 25:27',
              '«Что город разрушенный без стен, то человек, не владеющий духом своим.» Притчи Соломона 25:28',
              '«Как снег летом и дождь во время жатвы, так честь неприлична глупому.» Притчи Соломона 26:1',
              '«Как воробей вспорхнет, как ласточка улетит, так незаслуженное проклятье не сбудется.» Притчи Соломона 26:2',
              '«Не отвечай глупому на глупости его, чтобы и тебе не сделаться подобным ему;.» Притчи Соломона 26:4',
              '«Подрезывает себе ноги, терпит неприятности тот, кто дает словесное поручение глупцу.» Притчи Соломона 26:6',
              '«Видал ли ты человека, мудрого в глазах его? На глупого больше надежды, нежели на него.» Притчи Соломона 26:12',
              '«Ленивец в глазах своих мудрее семерых, отвечающих обдуманно.» Притчи Соломона 26:16',
              '«Как притворяющийся помешанным бросает огонь, стрелы и смерть, так — человек, который коварно вредит другу своему и потом говорит: "Я только пошутил".» Притчи Соломона 26:18-19',
              'Уголь — для жара и дрова — для огня, а человек сварливый — для разжжения ссоры.» Притчи Соломона 26:21',
              'Лживый язык ненавидит уязвляемых им, и льстивые уста готовят падение.» Притчи Соломона 26:28',
              ]

        p = mp[randint(0, len(mp) - 1)].split('Притчи')
        p[1] = "Притчи " + p[1]
        self.pr = p
        # self.pr = mp[0]
