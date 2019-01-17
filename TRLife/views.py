from django.shortcuts import get_object_or_404, render
from .models import Region, Substation, Transformer
import datetime
import json
import pandas as pd


def index(request):
    """Main"""
    region_list = Region.objects.order_by('name')
    context = {'region_list': region_list}

    return render(request, 'TRLife/home.html', context)


def detail_substation(request, se_short_name):
    """Retorna 404 ou carrega os dados do primeiro transformador da subestação"""
    substation = get_object_or_404(Substation, short_name=se_short_name)
    transformers = substation.transformer_set.all()
    transformer = transformers[0]
    return detail_transformer(request, se_short_name, transformer.name)


def detail_transformer(request, se_short_name, tr_name):
    """Carrega os dados do transformador"""
    substation = Substation.objects.get(short_name=se_short_name)
    tr_path_name = se_short_name+"_"+tr_name
    transformer = Transformer.objects.get(path_name=tr_path_name)

    # Data
    life_days, data_json = data_transformer(transformer)
    context = {'substation': substation, 'transformer': transformer, 'life_days': life_days, 'data_json': data_json}
    return render(request, 'TRLife/detail_substation.html', context)


def data_transformer(transformer):

    #Grafico
    df_chart = pd.read_excel(transformer.path_name + '.xlsx')
    x_arr = [x for x in df_chart['mes'] ]
    ieee_arr = [i for i in df_chart['IEEE'] ]
    fuzzy_arr = [ f for f in df_chart['Fuzzy'] ]
    carriel_arr = [c for c in df_chart['Carriel'] ]

    # Excel - resumo
    df = pd.read_excel('TRresumo.xlsx')
    df.set_index('TR', inplace=True)
    df_TR = df.loc[transformer.path_name]
    ieee_sum_pu = df_TR['ieee_sum']
    fuzzy_sum_pu = df_TR['fuzzy_sum']
    carriel_sum_pu = df_TR['carriel_sum']
    agua_mean = df_TR['agua_mean']
    oxigenio_mean = df_TR['oxigenio_mean']
    temp_mean = df_TR['temp_mean']
    start_excel_day = df_TR['start_excel_day']
    end_excel_day = df_TR['end_excel_day']

    # Life time
    install_date = transformer.install_date
    start_excel_day = datetime.date(start_excel_day.year, start_excel_day.month, start_excel_day.day)
    end_excel_day = datetime.date(end_excel_day.year, end_excel_day.month, end_excel_day.day)
    excel_days = (end_excel_day - start_excel_day).days
    if install_date < start_excel_day:
        before_days = (start_excel_day - install_date).days
    else:
        before_days = 0

    ieee_factor = (ieee_sum_pu / excel_days)
    fuzzy_factor = (fuzzy_sum_pu / excel_days)
    carriel_factor = (carriel_sum_pu / excel_days)

    real_life_days = excel_days
    ieee_life_days = int (excel_days/ieee_factor)
    fuzzy_life_days = int(excel_days/fuzzy_factor)
    carriel_life_days = int(excel_days/carriel_factor)

    before_years = round(before_days/365, 1)
    real_life_years = round(real_life_days/365, 1)
    ieee_life_years = round(ieee_life_days/365, 1)
    fuzzy_life_years = round(fuzzy_life_days/365, 1)
    carriel_life_years = round(carriel_life_days/365, 1)

    real_life = "{} + {} = {} anos".format(before_years, real_life_years, round(before_years+real_life_years, 1) )
    ieee_life = "{} + {} = {} anos".format(before_years, ieee_life_years,  round(before_years+ieee_life_years, 1))
    fuzzy_life = "{} + {} = {} anos".format(before_years, fuzzy_life_years,  round(before_years+fuzzy_life_years, 1))
    carriel_life = "{} + {} = {} anos".format(before_years, carriel_life_years, round(before_years+carriel_life_years, 1))

    agua, oxigenio = dga_classification(agua_mean, oxigenio_mean)
    expected_life = 40

    life_days = {'real': real_life,
                 'ieee': ieee_life,
                 'fuzzy': fuzzy_life,
                 'carriel': carriel_life,
                 'ieee_remaining': "{:.1f} anos".format(expected_life-ieee_life_years-before_years),
                 'fuzzy_remaining': "{:.1f} anos".format(expected_life-fuzzy_life_years-before_years),
                 'carriel_remaining': "{:.1f} anos".format(expected_life-carriel_life_years-before_years),
                 'agua':agua ,
                 'oxigenio':oxigenio,
                 'temperatura':round(temp_mean,1)}

    # x_arr = ["January", "February", "March", "April", "May", "June", "July"]
    # ieee_arr = [0, 10, 5, 2, 20, 30, 45]
    # carriel_arr = [1, 11, 6, 3, 21, 31, 46]
    # fuzzy_arr = [2, 12, 7, 4, 22, 32, 47]

    data = {'x_values': x_arr,
            'ieee_values':  ieee_arr,
            'fuzzy_values': fuzzy_arr,
            'carriel_values': carriel_arr
            }
    return (life_days, json.dumps(data))


def dga_classification(h2o, o2):
    h2o = round(h2o,2)
    o2 = int(o2)
    # O2
    if o2<6000:
        str_o2 = "{} ppm (baixo)".format(o2)
    elif o2<15000:
        str_o2 = "{} ppm (médio)".format(o2)
    else:
        str_o2 = "{} ppm (alto)".format(o2)

    #H2O
    if h2o < 0.5:
        str_h2o = "{}% (baixo)".format(h2o)
    elif h2o < 1.5:
        str_h2o = "{}% (normal)".format(h2o)
    elif h2o < 2.3:
        str_h2o = "{}% (alto)".format(h2o)
    else:
        str_h2o = "{}% (muito alto)".format(h2o)

    return (str_h2o, str_o2)



