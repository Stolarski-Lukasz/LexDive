from django.urls import path
from . import views

urlpatterns = [
    path('count_mtld_whole_text/', views.count_mtld_whole_text, name='count_mtld_whole_text'),
    path('count_mtld_whole_text_lemmas/', views.count_mtld_whole_text_lemmas, name='count_mtld_whole_text_lemmas'),
    path('count_hdd_whole_text/', views.count_hdd_whole_text, name='count_hdd_whole_text'),
    path('count_ttr_whole_text/', views.count_ttr_whole_text, name='count_ttr_whole_text'),
    path('count_ttr_whole_text_lemmas/', views.count_ttr_whole_text_lemmas, name='count_ttr_whole_text_lemmas'),
    path('count_ttr_split_text/', views.count_ttr_split_text, name='count_ttr_split_text'),
    path('count_ttr_split_text_lemmas/', views.count_ttr_split_text_lemmas, name='count_ttr_split_text_lemmas'),
    path('count_ttr_equal_text/', views.count_ttr_equal_text, name='count_ttr_equal_text'),
    path('count_ttr_equal_text_lemmas/', views.count_ttr_equal_text_lemmas, name='count_ttr_equal_text_lemmas'),
    path('count_herdans_c_whole_text/', views.count_herdans_c_whole_text, name='count_herdans_c_whole_text'),
    path('count_herdans_c_whole_text_lemmas/', views.count_herdans_c_whole_text_lemmas, name='count_herdans_c_whole_text_lemmas'),
    path('count_herdans_c_split_text/', views.count_herdans_c_split_text, name='count_herdans_c_split_text'),
    path('count_herdans_c_split_text_lemmas/', views.count_herdans_c_split_text_lemmas, name='count_herdans_c_split_text_lemmas'),
    path('count_herdans_c_equal_text/', views.count_herdans_c_equal_text, name='count_herdans_c_equal_text'),
    path('count_herdans_c_equal_text_lemmas/', views.count_herdans_c_equal_text_lemmas, name='count_herdans_c_equal_text_lemmas'),
    path('count_guirauds_r_whole_text/', views.count_guirauds_r_whole_text, name='count_guirauds_r_whole_text'),
    path('count_guirauds_r_whole_text_lemmas/', views.count_guirauds_r_whole_text_lemmas, name='count_guirauds_r_whole_text_lemmas'),
    path('count_guirauds_r_split_text/', views.count_guirauds_r_split_text, name='count_guirauds_r_split_text'),
    path('count_guirauds_r_split_text_lemmas/', views.count_guirauds_r_split_text_lemmas, name='count_guirauds_r_split_text_lemmas'),
    path('count_guirauds_r_equal_text/', views.count_guirauds_r_equal_text, name='count_guirauds_r_equal_text'),
    path('count_guirauds_r_equal_text_lemmas/', views.count_guirauds_r_equal_text_lemmas, name='count_guirauds_r_equal_text_lemmas'),
    path('count_uber_u_whole_text/', views.count_uber_u_whole_text, name='count_uber_u_whole_text'),
    path('count_uber_u_whole_text_lemmas/', views.count_uber_u_whole_text_lemmas, name='count_uber_u_whole_text_lemmas'),
    path('count_uber_u_split_text/', views.count_uber_u_split_text, name='count_uber_u_split_text'),
    path('count_uber_u_split_text_lemmas/', views.count_uber_u_split_text_lemmas, name='count_uber_u_split_text_lemmas'),
    path('count_uber_u_equal_text/', views.count_uber_u_equal_text, name='count_uber_u_equal_text'),
    path('count_uber_u_equal_text_lemmas/', views.count_uber_u_equal_text_lemmas, name='count_uber_u_equal_text_lemmas')
]
