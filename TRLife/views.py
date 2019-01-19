from django.shortcuts import get_object_or_404, render
from .models import Region, Substation, Transformer
import datetime
import json
#import pandas as pd


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

    life_days = {'real': 22,
                 'ieee': 23,
                 'fuzzy': 24,
                 'carriel': 25,
                 'ieee_remaining': "{:.1f} anos".format(3.56),
                 'fuzzy_remaining': "{:.1f} anos".format(4.67),
                 'carriel_remaining': "{:.1f} anos".format(7.8),
                 'agua':0.2 ,
                 'oxigenio':20000,
                 'temperatura':round(93.76,1)}

    x_arr = ["January", "February", "March", "April", "May", "June", "July"]
    ieee_arr = [0, 10, 5, 2, 20, 30, 45]
    carriel_arr = [1, 11, 6, 3, 21, 31, 46]
    fuzzy_arr = [2, 12, 7, 4, 22, 32, 47]

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



