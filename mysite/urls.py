from django.urls import path, include
from . import views

app_name = 'mysite'

urlpatterns = [
    path('', views.home, name="home"),
    path('apptesting/', include([
        # linki zajmujace sie obsluga uzytkownikow
        path("register", views.register_request, name="register"),
        path("login", views.login_request, name="login"),
        path("logout", views.logout_request, name="logout"),

        # linki do zarzadzania aplikacjami uzytkownika
        path("show_applications", views.show_applications, name="show_applications"),
        path("delete_application/<int:id>", views.delete_application, name="delete_application"),

        # linki do zarzadzania testami
        path("show_all_tests/", views.show_all_tests, name="show_all_tests"),
        path("show_tests/<int:id>", views.show_tests, name="show_tests"),
        path("delete_test/<int:app_id>/<int:test_id>", views.delete_test, name="delete_test"),

        # linki do zarzadzania krokami dla testow
        path("show_steps/<int:id>", views.show_steps, name="show_steps"),
        path("delete_step/<int:test_id>/<int:step_id>", views.delete_step, name="delete_step"),

        # Linki do podstron z opisami i informacjami
        path("wstep", views.wstep, name="wstep"),
        path("podzial-na-klasy-rownowaznosci", views.podzial_na_klasy_rownowaznosci,
             name="podzial-na-klasy-rownowaznosci"),
        path("analiza-wartosci-brzegowych", views.analiza_wartosci_brzegowych, name="analiza-wartosci-brzegowych"),
        path("testowanie-w-oparciu-o-tablice-decyzyjna", views.testowanie_w_oparciu_o_tablice_decyzyjna,
             name="testowanie-w-oparciu-o-tablice-decyzyjna"),
        path("testowanie-przejsc-miedzy-stanami", views.testowanie_przejsc_miedzy_stanami,
             name="testowanie-przejsc-miedzy-stanami"),
        path("testowanie-oparte-na-przypadkach-uzycia", views.testowanie_oparte_na_przypadkach_uzycia,
             name="testowanie-oparte-na-przypadkach-uzycia"),
        path("jak-pisac-przypadki-testowe", views.jak_pisac_przypadki_testowe, name="jak-pisac-przypadki-testowe"),
        path("about", views.about, name="about"),
    ]))
]
