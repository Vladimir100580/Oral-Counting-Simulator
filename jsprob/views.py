import time
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from random import randint
from .models import DataUser, Indexs
from django.contrib.auth import authenticate, login


def hello(request):
    answer = request.GET
    try:
        er = request.session['ti_contr']
    except:
        request.session['ti_contr'] = time.time() - 4
    # a = abs(float(request.session['ti_contr']) - time.time())
    if abs(float(request.session['ti_contr']) - time.time())<3 and 'intlg' not in answer and 'reg' not in answer:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')

        tab = Indexs.objects.get(pk=1)
        koler = tab.scor.split('$')
        idus = tab.fio.split('$')

        if ip in idus:
            koler[idus.index(ip)] = str(int(float(koler[idus.index(ip)])+1))
        else:
            idus.append(ip)
            koler.append('1')
        stid = ''
        stkol = ''
        i = 0
        for idu in idus:
            if (i+1) != len(idus): d = '$'
            else: d = ''
            stid = stid + str(idu) + d
            stkol = stkol + str(koler[i]) + d
            i += 1
        tab.fio = stid
        tab.scor = stkol
        tab.save()
        t=5/0

    if 'intlg' in answer or 'reg' in answer:
        request.session['ti_contr'] = time.time() - 3
    else: request.session['ti_contr'] = time.time()

    user_id = request.user.username
    fl0='0'
    if (user_id != ''):
        nm = request.user.first_name.split('$#$%')
        print('nm', nm)
        if len(nm)==4: fl0='1'
        nm = ', ' + nm[1]
        fl=1
    else:
        nm=''
        fl=0
    # if request.method == 'GET':
        #answer = request.GET
    if 'reg' in answer: return redirect('regist')
    if 'intlg' in answer:
        lg = answer.__getitem__('lg')
        if len(lg)<3: return redirect('home')
        if User.objects.filter(username=lg).exists()==1:
            user = authenticate(request, username=lg, password='4591423')
            login(request, user)
            return redirect('home')
        else: return render(request, 'jsprob/nezar.html')

    return render(request, 'jsprob/priv.html', {'nm':nm, 'fl':fl, 'fl0': fl0})


def regist(request):
    #return redirect('logout')
    if request.method == 'GET':
        answer = request.GET
        if 'fam' in answer and 'name' in answer and 'lg' in answer :
            f = answer.__getitem__('fam').replace(' ', '').capitalize()
            n = answer.__getitem__('name').replace(' ', '').capitalize()
            if f == '' or n == '': return redirect('regist')
            k = answer.__getitem__('kl').replace(' ', '')
            lg = answer.__getitem__('lg')
            if len(f) < 2 or len(n) < 2 or len(f) > 25 or len(n) > 25 or len(k) > 25 or len(lg) > 30 or len(lg)<3 :
                return redirect('regist')
            if User.objects.filter(username=lg).exists():
                return render(request, 'jsprob/ujuse.html')
                # user = authenticate(request, username=lg, password='4591423')
                # if user is not None:
                #     login(request, user)
                # return redirect('home')
            else:
                DataUser(log=lg, scores=0, fik=f + ' ' + n + ' ' + k).save()
                user = User.objects.create_user(lg, '', '4591423', first_name=f +'$#$%' + n +'$#$%'+k)
                user.save()
                user = authenticate(request, username=lg, password='4591423')
                login(request, user)
                return render(request, 'jsprob/uspreg.html')
    return render(request, 'jsprob/registr.html')


def itog(request):
    ud = request.COOKIES.get('lelrec15').split('$')
    if ud[0] != 'e':
        if float(ud[0]) < float(ud[1]):
            DataUser.objects.filter(log=request.session['ustns4usen']).update(scoresl5=ud[1])

    usna = request.user.username
    if (usna == None): return redirect('home')
    tts = request.COOKIES.get('totsumm').split('(#)$)')
    bonz = int(float(tts[2]) * 100)
    sum = int(float(tts[0])) + bonz
    bon = ' 100 X ' + str(int(float(tts[2]))) + ':'
    tx = ['неплохо', 'совсем неплохо', 'очень хорошо', 'прекрасно', 'просто превосходно'][min(sum // 50000, 4)]
    tt = DataUser.objects.get(log=usna)
    ds = 0
    scold = 0
    t = ' очков'
    if (sum // 10) % 10 != 1:
        if sum % 10 == 2 or sum % 10 == 3 or sum % 10 == 4: t = ' очка'
        if sum % 10 == 1: t = ' очко'
    if tt.pop != 1:
        scold = tt.scores
        ds = int(float(sum) - scold)
        if ds > 0:
            fl = 1
            DataUser.objects.filter(log=usna).update(scores=sum, pravil=(int(float(tts[1])+ float(tts[2]))), bezosh=tts[2])
        if ds < 0:
            fl = 2
        if ds == 0:
            fl = 3
    else:
        if sum > 0:
            fl = 4
            DataUser.objects.filter(log=usna).update(scores=sum, pravil=(int(float(tts[1])+ float(tts[2]))), bezosh=tts[2])
        else:
            DataUser.objects.filter(log=usna).update(scores=sum, pravil=(int(float(tts[1])+ float(tts[2]))), bezosh=tts[2])
            fl = 5

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
          '«Когда мудрость войдет в сердце твое, и знание будет приятно душе твоей, тогда рассудительность будет оберегать тебя, разум будет охранять тебя» Притчи Соломона 2:10-11',
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
          '«Приложи сердце твое к учению и уши твои — к умным словам.» Притчи Соломона 23:12'
          ]

    pr = mp[randint(0, len(mp) - 1)].split('Притчи')
    return render(request, 'jsprob/itog.html', {'t':t, 'tx':tx, 'ds':str(ds), 'sum':str(sum), 'scold':str(scold),
                          'fl':fl, 'txt3':pr[0], 'txt4':'Притчи' + pr[1], 'pr': int(float(tts[1]) + float(tts[2])),
                          'bz':int(float(tts[2])), 'lv1':tts[3], 'lv2':tts[4], 'lv3':tts[5], 'lv4':tts[6], 'lv5':tts[7],
                          'bon':bon, 'bonz':bonz, 'su':str(sum-bonz)})


def toptab(request):
    tt = []
    usna = request.user.username
    n=0
    for r in DataUser.objects.order_by('-scores')[:100]:
        if r.scores!=0:
            n+=1
            fio = str(n) + ') ' + r.pole1
            if r.log != usna:
                if n % 3 == 1:
                    tt.append(['1', fio, r.scores, r.pole2.split('$')[0] + '/' + r.pole2.split('$')[2]])
                if n % 3 == 0:
                    tt.append(['4', '', '', '', '', '', '', '', '', '', fio, r.scores, r.pole2.split('$')[0]+ '/' + r.pole2.split('$')[2]])
                if n % 3 == 2:
                    tt.append(['3', '', '', '', '', '', '', fio, r.scores, r.pole2.split('$')[0]+ '/' + r.pole2.split('$')[2]])
            else:
                tt.append(['2', '', '', '', fio, r.scores, r.pole2.split('$')[0]+ '/' + r.pole2.split('$')[2]])
    return render(request, 'jsprob/toptab.html', {'tt':tt})


def toplvl(request):
    tt = [[] for i in range(5)]
    try:
        usna = request.user.first_name.replace('$#$%', ' ')
    except: usna =''
    n=0
    m=0
    topzn = Indexs.objects.all()
    for topz in topzn:
        n+=1
        if n>1:
            sctablv = topz.scor.split('_')
            del sctablv[len(sctablv) - 2:len(sctablv)]
            namtablv = topz.fio.split('$^%^')
            del namtablv[len(namtablv) - 2:len(namtablv)]
            i=0
            for nml in namtablv:
                if sctablv[i]!=0:
                    if i==0: tt[n-2].append(str(n-1))
                    if nml != usna:
                        tk = [str(i % 2), str(i+1) + '. ' + nml, sctablv[i]]
                    else:
                        tk=['2', str(i+1) + '. ' + nml, sctablv[i]]
                    tt[n - 2].append(tk)
                i+=1
    return render(request, 'jsprob/toplvl.html', {'tt':tt})


def reset(request):
    if (request.user.is_superuser) != True: return redirect('home')
    if request.method == 'GET':
        answer = request.GET
        if 'res' in answer:
            allpolz = DataUser.objects.all()
            for allp in allpolz:
                if allp.pole2.count('$')!=7:
                    allp.pole2 = '0$1$0$0$0$0$0$0'
                p2 = allp.pole2.split('$')
                po = '1'
                if float(p2[3]) + float(p2[4]) + float(p2[5]) + float(p2[6]) + float(p2[7]) > 0: po = '2'
                allp.pole2 = '0$' + po + '$0$' + p2[3] + '$' + p2[4] + '$' + p2[5] + '$' + p2[6] + '$' + p2[7]
                allp.scores = 0
                allp.save()
            allpolz = TopTabllev.objects.all()
            i=0
            for allp in allpolz:
                i+=1
                if i>1:
                    allp.fio = 'Иванов Николай 11Б$^%^Петрова Нина Константиновна$^%^Буренко Алексей Сергеевич$^%^Сидоров Илья 10$^%^Мельников Григорий 8$^%^Светлоусов Женя 6$^%^Муртазина Оля 4$^%^B$^%^F'
                    allp.scor = '10000_8000_6000_4000_3000_2000_1000_500_300'
                    allp.save()
            return redirect('home')
    return render(request, 'jsprob/reset.html')


def level1(request):
    usna = request.user.username
    request.session['ustns4usen'] = usna
    usefio = request.user.first_name.split('$#$%')
    # if DataUser.objects.filter(log=usna).exists() != 1:
    #     DataUser(log=usna, scores=0, pole1=fio, pole2='0$1$0$0$0$0$0$0').save()
    tt = DataUser.objects.get(log=usna)
    if tt.scores>0:
        DataUser.objects.filter(log=usna).update(%s=(tt.pop+1))
    # Defuser(fio, 1, request.session['ustns4usen'])
    return render(request, 'jsprob/level1.html', {'nm':usefio[1]})


def level2(request):
    ud = request.COOKIES.get('lelrec15').split('$')
    usefio = request.user.first_name.split('$#$%')
    if ud[0]!='e':
        if float(ud[0]) < float(ud[1]):
            DataUser.objects.filter(log=request.session['ustns4usen']).update(scoresl1=ud[1])
    return render(request, 'jsprob/level2.html', {'nm':usefio[1]})


def level3(request):
    ud = request.COOKIES.get('lelrec15').split('$')
    if ud[0] != 'e':
        if float(ud[0]) < float(ud[1]):
            DataUser.objects.filter(log=request.session['ustns4usen']).update(scoresl2=ud[1])
    return render(request, 'jsprob/level3.html')


def level4(request):
    ud = request.COOKIES.get('lelrec15').split('$')
    if ud[0] != 'e':
        if float(ud[0]) < float(ud[1]):
            DataUser.objects.filter(log=request.session['ustns4usen']).update(scoresl3=ud[1])
    return render(request, 'jsprob/level4.html')


def level5(request):
    ud = request.COOKIES.get('lelrec15').split('$')
    if ud[0] != 'e':
        if float(ud[0]) < float(ud[1]):
            DataUser.objects.filter(log=request.session['ustns4usen']).update(scoresl4=ud[1])
    return render(request, 'jsprob/level5.html')


def list1(request):
    Vyb = Vyborka(0,10)
    usefio = request.user.first_name.split('$#$%')
    fio = usefio[0] + ' ' + usefio[1] + ' ' + usefio[2]
    Du = Defuser(fio, 1, request.session['ustns4usen'])
    return render(request, 'jsprob/list1.html', {'tas1': Vyb.t1, 'tas2': Vyb.t2, 'tasz': Vyb.tz, 'otv': Vyb.ot, 'minsc':Du.minsc, 'scnow':Du.scnow, 'sclvus':Du.sclvus, 'fl00':Du.fl00 })

def list2(request):
    Vyb = Vyborka(10, 20)
    usefio = request.user.first_name.split('$#$%')
    fio = usefio[0] + ' ' + usefio[1] + ' ' + usefio[2]
    Du = Defuser(fio, 2, request.session['ustns4usen'])
    return render(request, 'jsprob/list2.html',
                  {'tas1': Vyb.t1, 'tas2': Vyb.t2, 'tasz': Vyb.tz, 'otv': Vyb.ot, 'minsc': Du.minsc, 'scnow': Du.scnow,
                   'sclvus': Du.sclvus, 'fl00': Du.fl00})

def list3(request):
    Vyb = Vyborka(20, 30)
    usefio = request.user.first_name.split('$#$%')
    fio = usefio[0] + ' ' + usefio[1] + ' ' + usefio[2]
    Du = Defuser(fio, 3, request.session['ustns4usen'])
    return render(request, 'jsprob/list3.html',
                  {'tas1': Vyb.t1, 'tas2': Vyb.t2, 'tasz': Vyb.tz, 'otv': Vyb.ot, 'minsc': Du.minsc, 'scnow': Du.scnow,
                   'sclvus': Du.sclvus, 'fl00': Du.fl00})


def list4(request):
    Vyb = Vyborka(30, 40)
    usefio = request.user.first_name.split('$#$%')
    fio = usefio[0] + ' ' + usefio[1] + ' ' + usefio[2]
    Du = Defuser(fio, 4, request.session['ustns4usen'])
    return render(request, 'jsprob/list4.html',
                  {'tas1': Vyb.t1, 'tas2': Vyb.t2, 'tasz': Vyb.tz, 'otv': Vyb.ot, 'minsc': Du.minsc, 'scnow': Du.scnow,
                   'sclvus': Du.sclvus, 'fl00': Du.fl00})


def list5(request):
    Vyb = Vyborka(40, 50)
    usefio = request.user.first_name.split('$#$%')
    fio = usefio[0] + ' ' + usefio[1] + ' ' + usefio[2]
    Du = Defuser(fio, 5, request.session['ustns4usen'])
    return render(request, 'jsprob/list5.html',
                  {'tas1': Vyb.t1, 'tas2': Vyb.t2, 'tasz': Vyb.tz, 'otv': Vyb.ot, 'minsc': Du.minsc, 'scnow': Du.scnow,
                   'sclvus': Du.sclvus, 'fl00': Du.fl00})


class Examples:
    def __init__(self, rab, mm):
        otvs = [[''] * 1 for i in range(50)]  # №задачи (кол-во вариантов -1), количество задач (№ коретжа)
        tasks = [[''] * 1 for i in range(50)]  # №задачи (кол-во вариантов -1), количество задач (№ коретжа)

        for r in range(0, rab):
            # Устный счет
            y = 0
            # сложение
            if mm==0:
                provsov = [[0] * 3 for i in range(11)]  # обнуление массива контроля повторений
                for z in range(0, 5):
                    while True:
                        fl = 0
                        a = randint(2, 8)
                        b = randint(1, 10 - a)
                        mas = provsov
                        for d in range(0, 5):  # все 5 используя предыдущие
                            if (mas[d][0] == a) and (mas[d][1] == b) or (mas[d][0] == b) and (mas[d][1] == a)\
                                    or (mas[d][2] == a+b):
                                fl = 1
                        if fl == 0:
                            provsov[z][0] = a
                            provsov[z][1] = b
                            provsov[z][2] = a+b
                            tasks[y + z][r] = str(a) + '+' + str(b) + '='
                            otvs[y + z][r] = '0' # otvs[y + z][r] = str(a + b)
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
                            if (mas[d][0] == a) and (mas[d][1] == b) or (mas[d][0] == b) and (mas[d][1] == a) or (mas[d][2] == a-b):
                                fl = 1
                        if fl == 0:
                            provsov[z - 5][0] = a
                            provsov[z - 5][1] = b
                            provsov[z - 5][2] = a-b
                            tasks[y + z][r] = str(a) + '–' + str(b) + '='
                            otvs[y + z][r] = '0' # otvs[y + z][r] = str(a - b)
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
                            if (a + b) % 10 >= int(1.5 * (z - 10)) and (a+b)!=11:
                                break
                        mas = provsov
                        for d in range(0, 5):  # все 5 используя предыдущие
                            if (mas[d][0] == a) and (mas[d][1] == b) or (mas[d][0] == b) and (mas[d][1] == a) or (mas[d][2] == a+b):
                                fl = 1
                        if fl == 0:
                            provsov[z - 10][0] = a
                            provsov[z - 10][1] = b
                            provsov[z - 10][2] = a+b
                            while True:
                                fl0 = 0
                                if (randint(0, 1) == 0):
                                    a = a + 10 * randint((z - 10), (z - 10) * 2)
                                else:
                                    b = b + 10 * randint((z - 10), (z - 10) * 2)
                                prst = str(a + b)
                                for d in range(0, 10):
                                    if prst.find(str(d) + str(d)) != -1:
                                        a=a%10
                                        b=b%10
                                        fl0 = 1
                                if fl0==0: break
                            tasks[y + z][r] = str(a) + '+' + str(b) + '='
                            otvs[y + z][r] = str(a + b)
                            break
                lg = y + 11
                pg = y + 14
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
                                    if i==0:
                                        if str(a).find(str(d) + str(d)) != -1:
                                            a=a%10
                                            b=b%10
                                            fl0 = 1
                                    if i==1:
                                        if str(b).find(str(d) + str(d)) != -1:
                                            a = a % 10
                                            b = b % 10
                                            fl0 = 1
                                if fl0==0: break
                            if (i == 0):
                                tasks[y + z][r] = str(a + b) + '–' + str(b) + '='
                                otvs[y + z][r] = str(a)
                            else:
                                tasks[y + z][r] = str(a + b) + '–' + str(a) + '='
                                otvs[y + z][r] = str(b)
                            break

            if mm==20:
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
                            if (mas[d][0] == a) or (mas[d][1] == b) or (mas[d][0] == b) or (mas[d][1] == a) or (mas[d][2] == a+b):
                                fl = 1
                        if fl == 0:
                            provsov[z - 20][0] = a
                            provsov[z - 20][1] = b
                            provsov[z - 20][2] = a+b
                            a = a + i - 100
                            if (randint(0, 1) == 0):
                                tasks[y + z][r] = str(a) + '+' + str(b) + '='
                            else:
                                tasks[y + z][r] = str(b) + '+' + str(a) + '='
                            otvs[y + z][r] = str(a + b)
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
                            tasks[y + z][r] = str(a + b) + '–' + str(a) + '='
                            otvs[y + z][r] = str(b)
                            break

            if mm==30:
                # умножение на 10n
                provsov = [[0] * 2 for i in range(11)]
                for z in range(30, 35):
                    while True:
                        fl = 0
                        a = randint(1, 9)
                        a = 100 + a + 100 * randint(int((z - 30) * 0.4), int((z - 30) * 0.8))
                        b = randint(2, 9)
                        prst = str(a*b)
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
                                tasks[y + z][r] = str(a) + '•' + str(b) + '='
                            else:
                                tasks[y + z][r] = str(b) + '•' + str(a) + '='
                            otvs[y + z][r] = str(a * b)
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
                                tasks[y + z][r] = str(a) + '•' + str(b) + '='
                            else:
                                tasks[y + z][r] = str(b) + '•' + str(a) + '='
                            otvs[y + z][r] = str(a * b)
                            break

            if mm==40:
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
                            tasks[y + z][r] = str(a * b) + ':' + str(b) + '='
                            otvs[y + z][r] = str(a)
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
                            tasks[y + z][r] = str(a * b) + ':' + str(b) + '='
                            otvs[y + z][r] = str(a)
                            break

        self.tas = tasks
        self.ot = otvs


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
                    tasks1.append(float(tasks[r][:x]) + otvs + (r-m)**2)
                    tasksz.append(z)
                    tasks2.append(float(tasks[r][x + 1:len(tasks[r]) - 1]))
        # otvs = []
        # for i in range(m, n):
        #     otvs.append(float(Ex.ot[i][0]))

        self.t1 = tasks1
        self.t2 = tasks2
        self.tz = tasksz
        self.ot = otvs


class Defuser:
    def __init__(self, fio, lv, usna):
        krit = 'scoresl' + str(lv)
        mas = [i for i in DataUser.objects.order_by('-'+krit).values_list(krit, 'fik')][:10]
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
            scnow = 0        # сколько очков у игрока в ТОП-е

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
            if i == (lv+3):
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
        i=1
        while i==1:
            i=0
            for z in range(1, len(sctablv)):
                if float(sctablv[z-1])<float(sctablv[z]):
                    sctablv[z - 1], sctablv[z] = sctablv[z], sctablv[z - 1]
                    ustablv[z - 1], ustablv[z] = ustablv[z], ustablv[z - 1]
                    i = 1
        p2 = ''
        p1 = ''
        for i in range(9):
            if i!=8:
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
            sctablv[ustablv.index(fio)]=re
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