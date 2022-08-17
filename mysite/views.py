from cgi import test
from re import template
from urllib import response
from django.shortcuts import render, redirect
from .forms import NewApplicationForm, NewUserForm, NewTestForm, NewStepForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseForbidden
from django.utils import translation

from .models import Application, Test, TestStep


# Create your views here.
def home(request):
    return redirect('/apptesting/wstep')


# rejstracja uzytkownikow
def register_request(request):
    translation.activate('pl')
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            # jesli rejstracja sie powiedzie to tworze nowego uzytkownika w bazie i odrazu go lguje
            user = form.save()
            login(request, user)
            return redirect("mysite:home")

    form = NewUserForm()
    return render(request=request, template_name="mysite/register.html", context={"register_form": form})


# logowanie sie
def login_request(request):
    translation.activate('pl')

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # jesli dane sie beda zgadzac to loguje uzytkownika
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("mysite:home")

    form = AuthenticationForm()
    return render(request=request, template_name="mysite/login.html", context={"login_form": form})


# wylogowywanie sie
def logout_request(request):
    logout(request)
    return redirect("mysite:home")


# wyswietlanie i zarzadzanie danymi testowania
def show_applications(request):
    # jesli zostal wykonany POST to znaczy ze uzytkownik wypelnil formularz ddania nowej aplikacji i wtedy zajmujemy sie tymi danymi
    # w innych przypadkach poprostu wyswietalmy formularz i obecne dane
    if request.user.is_authenticated:
        if request.method == "POST":
            form = NewApplicationForm(request.POST)
            if form.is_valid():
                n = form.cleaned_data['name']
                Application.objects.create(owner=request.user, name=n)
                return redirect('mysite:show_applications')

        form = NewApplicationForm()

        # przypisuje wszystkie apkilacje danego uzytkownika
        user_apps = Application.objects.filter(owner=request.user)

        return render(request, template_name='mysite/applications.html', context={'form': form, 'apps': user_apps})

    return redirect('mysite:home')


def delete_application(request, id):
    # sprawdzam czy obecny uzytkownik jest wlascicielem tej aplikacji
    if request.user.is_authenticated:
        app = Application.objects.get(pk=id)
        if app.owner == request.user:
            app.delete()
            return redirect('mysite:show_applications')
    return HttpResponseForbidden()


# wysiwtlanie i zarzadzanie testami
def show_tests(request, id):
    # jesli zostal wykonany POST to znaczy ze uzytkownik wypelnil formularz ddania nowego testu i wtedy zajmujemy sie tymi danymi
    # w innych przypadkach poprostu wyswietalmy formularz i obecne dane
    if request.user.is_authenticated:
        app_ = Application.objects.get(pk=id)

        if request.method == "POST":
            form = NewTestForm(request.POST)
            if form.is_valid():
                n = form.cleaned_data['name']
                res = form.cleaned_data['result']
                if app_.owner == request.user:
                    Test.objects.create(app=app_, name=n, result=res)
                    return redirect('/show_tests/' + str(id))

        form = NewTestForm()

        # sprawdzam czy uzytkownik ma prawo i jesli tak to zwracam wsyztskie testy danej aplikacji
        if app_.owner == request.user:
            tests = Test.objects.filter(app=app_)
            return render(request, template_name='mysite/tests.html',
                          context={'form': form, 'tests': tests, 'app_id': id, 'app_name': app_.name})

    return redirect('mysite:home')


def delete_test(request, app_id, test_id):
    # sprawdzam czy obecny uzytkownik jest wlascicielem tej aplikacji
    if request.user.is_authenticated:
        app = Application.objects.get(pk=app_id)
        if app.owner == request.user:
            # znajduje odpowiedni test
            t = Test.objects.get(pk=test_id)
            t.delete()
            return redirect('/show_tests/' + str(app_id))
    return HttpResponseForbidden()


def show_all_tests(request):
    # jesli uzytwkonik jest zalogowany to wyswielta wszytskie testy z jego wszytskich aplikacji
    if request.user.is_authenticated:
        apps = Application.objects.filter(owner=request.user)
        tests = []
        for app_ in apps:
            tests += [[app_, x] for x in Test.objects.filter(app=app_.id)]

        return render(request, template_name='mysite/all_tests.html', context={'tests': tests})
    return HttpResponseForbidden()


# wyswietlanie i zarzadzanie krokami dla tesow
def show_steps(request, id):
    # jesli uzytkownik jest zalogowany i jest wlascicielem odpowiedniego testu
    # to moze wyswietlac kroki oraz je dodawac/usuwac
    if request.user.is_authenticated:
        test_ = Test.objects.get(pk=id)
        if test_.app.owner == request.user:
            if request.method == "POST":
                form = NewStepForm(request.POST)
                if form.is_valid():
                    desc = form.cleaned_data['description']
                    req = form.cleaned_data['requirements']
                    TestStep.objects.create(test=test_, description=desc, requirements=req)
                    return redirect('/show_steps/' + str(id))
            # jesli byl GET to znaczy ze uzytkownik nie wypelnil jeszcze formularza dodania wiec wyswietlam wczesniejsze dane i pusty formularz
            form = NewStepForm()
            if test_.app.owner == request.user:
                steps = TestStep.objects.filter(test=test_)
                return render(request, template_name='mysite/steps.html',
                              context={'form': form, 'steps': steps, 'test_name': test_.name,
                                       'app_name': test_.app.name})

    return HttpResponseForbidden()


def delete_step(request, test_id, step_id):
    # sprawdzam czy obecny uzytkownik jest wlascicielem tego testu
    if request.user.is_authenticated:
        step_ = TestStep.objects.get(pk=step_id)
        if step_.test.app.owner == request.user:
            # znajduje odpowiedni krok
            s = TestStep.objects.get(pk=step_id)
            s.delete()
            return redirect('/show_steps/' + str(test_id))
    return HttpResponseForbidden()


# wyswietlanie opisow i informacji dla odpowiednich podstron
def wstep(request):
    print('dupa')
    return render(request, template_name="mysite/opisy/intro.html")


def podzial_na_klasy_rownowaznosci(request):
    if request.user.is_authenticated:
        return render(request, template_name="mysite/opisy/podzial_na_klasy.html")
    return redirect('mysite:home')


def analiza_wartosci_brzegowych(request):
    if request.user.is_authenticated:
        return render(request, template_name="mysite/opisy/wartosci_brzegowe.html")
    return redirect('mysite:home')


def testowanie_w_oparciu_o_tablice_decyzyjna(request):
    if request.user.is_authenticated:
        return render(request, template_name="mysite/opisy/tablica_decyzyjna.html")
    return redirect('mysite:home')


def testowanie_przejsc_miedzy_stanami(request):
    if request.user.is_authenticated:
        return render(request, template_name="mysite/opisy/przejscia_miedzy_stanami.html")
    return redirect('mysite:home')


def testowanie_oparte_na_przypadkach_uzycia(request):
    if request.user.is_authenticated:
        return render(request, template_name="mysite/opisy/przypadki_uzycia.html")
    return redirect('mysite:home')


def jak_pisac_przypadki_testowe(request):
    if request.user.is_authenticated:
        return render(request, template_name="mysite/opisy/jak_pisac_przypadki.html")
    return redirect('mysite:home')
