# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.utils.timezone import now
from django.views import generic
from django.contrib.auth import logout, login
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import UserForm, CommentForm, CriticForm, ActForm, ComForm, TempUserForm
from .models import Act, Critic, Comment, Community


def index(request):
    acts = Act.objects.filter(id__in=Critic.objects.filter(is_approved=True).values_list('act', flat=True)).distinct()
    item_list = []
    for act in acts:
        dummy_dict = {"act": act,
                      "critics": list(Critic.objects.filter(act=act, is_approved=True).order_by('-pub_date')[:2])}
        item_list.append(dummy_dict)
    print item_list[0]['critics'][0].pub_date
    sorted_list = sorted(item_list, key=lambda k: k['critics'][0].pub_date, reverse=True)
    return render(request, 'main/index.html', {'item_list': sorted_list})


def acts(request):
    act_list = Act.objects.exclude(image__exact='').order_by('-create_date')
    page = request.GET.get('page', 1)

    paginator = Paginator(act_list, 9)
    try:
        acts = paginator.page(page)
    except PageNotAnInteger:
        acts = paginator.page(1)
    except EmptyPage:
        acts = paginator.page(paginator.num_pages)

    return render(request, 'main/acts.html', {'acts': acts})


def critic(request):
    critic_list = Critic.objects.filter(pub_date__lte=timezone.now(), is_approved=True).order_by('-pub_date')
    page = request.GET.get('page', 1)

    paginator = Paginator(critic_list, 10)
    try:
        critics = paginator.page(page)
    except PageNotAnInteger:
        critics = paginator.page(1)
    except EmptyPage:
        critics = paginator.page(paginator.num_pages)

    return render(request, 'main/critics.html', {'critics': critics})


def addCritic(request):
    acts = Act.objects.all().order_by("name")
    if request.method == "POST":
        form = CriticForm(request.POST)
        if form.is_valid():
            critic = form.save(commit=False)
            critic.editor = request.user
            critic.pub_date = now()
            critic.save()

            act = form.cleaned_data['act']
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            send_mail(
                u'Yeni eleştiri yazıldı',
                '\nYazar: ' + request.user.username + '\nOyun: ' + act.name + u'\nBaşlık: ' + title + u'\n\nEleştiri: \n' + text,
                'veperdeinfo@gmail.com',
                ['veperdeinfo@gmail.com'],
                fail_silently=True,
            )

            return HttpResponseRedirect('../kullanici/')
    else:
        form = CriticForm()

    acto = Act.objects.all().order_by("-create_date").first()
    return render(request, 'main/addCritic.html', {'form': form, 'acts': acts, 'acto': acto})


class DetailView(generic.DetailView):
    model = Act
    template_name = 'main/detail.html'

    def get_queryset(self):
        return Act.objects.all()


def critic_detail(request, pk):
    # TODO gosterimde sikinti var editorle girilen metinde
    if request.method == "POST":
        critic = get_object_or_404(Critic, pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.critic = critic
            comment.save()
            return HttpResponseRedirect('../%d/' % int(pk))
    else:
        critic = Critic.objects.get(pk=pk)
        form = CommentForm()
    fb_share_url = request.build_absolute_uri() + '&display=popup'
    return render(request, 'main/c_detail.html', {'critic': critic, 'form': form, 'fb_share': fb_share_url})


def addUser(request):
    if request.method == "POST":
        username = request.POST.get('username', '').replace('_', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        # import pdb; pdb.set_trace()
        message = None
        if User.objects.filter(username=username).count() > 0:
            message = u"Bu kullanıcı adı ile daha önce kayıt yapılmış. Lütfen yeni bir kullanıcı adı belirleyiniz."
        if User.objects.filter(email=email).count() > 0:
            message = u"Bu e-posta ile daha önce kayıt yapılmış. Lütfen yeni bir e-posta belirleyiniz."
        if message:
            return render(request, 'main/contact.html', {"message": message,
                                                         "username": username, "email": email})
        new_user = User.objects.create_user(username,
                                            email,
                                            password,
                                            is_staff=False,
                                            is_superuser=False)
        login(request, new_user)
        # redirect, or however you want to get to the main view
        return HttpResponseRedirect('../kullanici/')

    return render(request, 'main/contact.html', {})


def communityDetail(request, pk):
    community = Community.objects.get(pk=pk)
    return render(request, 'main/communityDetail.html', {'community': community})


def profile(request):
    if request.method == "POST":
        form = TempUserForm(request.POST)
        user = request.user
        if form.is_valid():
            user.email = form.cleaned_data['email']
            user.save()
            return HttpResponseRedirect('../')
    else:
        form = UserForm(instance=request.user)
    return render(request, 'main/profile.html', {'form': form})


def addAct(request):
    # TODO communities alfabetik sirada gelmiyor
    if request.user.is_superuser:
        return HttpResponseRedirect('/admin/main/act/add/')
    else:
        if request.method == "POST":
            community_id = request.POST.get('communityId', '')
            act_name = request.POST.get('actName', '')
            form = ActForm(request.POST)
            form2 = ComForm(request.POST)
            if form2.is_valid():
                community = form2.save(commit=False)
                community.save()
                communities = Community.objects.filter(create_date__lte=timezone.now()).order_by("name")
                return render(request, 'main/addAct.html', {'form': form, 'form2': form2,
                                                            'communitys': communities,
                                                            'community': community})
            elif community_id and act_name:
                community = Community.objects.filter(id=community_id).first()
                act = Act.objects.create(name=act_name, community=community)
                return HttpResponseRedirect('../yaziekle/')
        else:
            form = ActForm()
            form2 = ComForm()
        communities = Community.objects.filter(create_date__lte=timezone.now()).order_by("name")
        return render(request, 'main/addAct.html', {'form': form, 'form2': form2, 'communitys': communities})


def approveCritic(request):
    if request.user.is_superuser:
        critics = Critic.objects.filter(pub_date__lte=timezone.now(), is_approved=False)
    else:
        return redirect('login')
    return render(request, 'main/approveCritic.html', {'critics': critics})


def approveC(request, pk):
    critic = Critic.objects.get(pk=pk)
    critic.approve()
    send_mail(
        'Eleştiriniz yayında :)',
        critic.act.name + ' oyunu hakkındaki ' + critic.title + ' başlıklı eleştiriniz yayınlanmıştır. Fikirlerinizi paylaşarak tiyatro dünyasına yaptığınız katkıdan dolayı size çok teşekkür ederiz.' +
        ' www.veperde.com/elestiriler/' + str(critic.id),
        'veperdeinfo@gmail.com',
        [critic.editor.email],
        fail_silently=True,
    )
    return HttpResponseRedirect('../elestirionayla/')


def deleteComment(request, pk):
    comment = Comment.objects.get(pk=pk)
    comment.delete()
    return HttpResponseRedirect('/elestiriler/%d/' % comment.critic.id)


def deleteCritic(request, pk):
    if request.user.is_superuser:
        critic = Critic.objects.get(pk=pk)
        critic.delete()
        return redirect('/elestirionayla/')
    else:
        return redirect('elestiriler')


def updateCritic(request, pk):
    critic = get_object_or_404(Critic, pk=pk)
    if critic.editor.username != request.user.username:
        return redirect('/elestiriler/%d/' % critic.id)
    if request.method == "POST":
        form = CriticForm(request.POST, instance=critic)
        if form.is_valid():
            critic = form.save(commit=False)
            editor = request.user
            critic.save()
            return redirect('/elestiriler/%d/' % critic.id)
    else:
        form = CriticForm(instance=critic)
    return render(request, 'main/updateCritic.html', {'form': form})


def changeAct(request, pk):
    # TODO bunu admin panelinden front ende tasicaz
    return HttpResponseRedirect('/admin/main/act/%d/change/' % int(pk))
