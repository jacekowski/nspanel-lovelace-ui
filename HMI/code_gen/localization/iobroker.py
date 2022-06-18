import os
import json
from collections import defaultdict

keys = {
    'frontend.ui.card.light.brightness':                 'lights.Brightness',
#    'frontend.ui.card.light.brightness':                 'lights.Color',
    'frontend.ui.card.light.color_temperature':          'lights.Temperature',
    'backend.component.binary_sensor.state.window.off':  'window.closed',
    'backend.component.binary_sensor.state.window.on':   'window.opened',
    'backend.component.binary_sensor.state.door.off':    'door.closed',
    'backend.component.binary_sensor.state.door.on':     'door.opened',
    'frontend.ui.card.lock.lock':                        'lock.LOCK',
    'frontend.ui.card.lock.unlock':                      'lock.UNLOCK',
    'frontend.ui.card.cover.position':                   'blinds.Position',
    'frontend.ui.card.climate.currently':                'thermostat.Currently',
    'frontend.ui.panel.config.devices.entities.state':   'thermostat.State',
    'frontend.ui.card.climate.operation':                'thermostat.Action',
}


langs = ["en_US", "de_DE", "nl_NL", "da_DK", "es_ES", "fr_FR", "it_IT", "ru_RU"]


def build_locale_filestring(locale):
    if locale in ["zh_CN", "zh_Hans_CN", "zh_Hans"]:
        locale = "zh-Hans"
    elif locale in ["zh_TW", "zh_Hant_TW", "zh_Hant"]:
        locale = "zh-Hant"
    elif locale == "en_GB":
        locale = "en-GB"
    elif locale == "pt_BR":
        locale = "pt-BR"
    else:
        locale = locale.split("_")[0]

    filename = f"{locale}.json"
    dir_path = os.getcwd()
    path_frontend_file = os.path.join(dir_path, "apps", "nspanel-lovelace-ui", "luibackend", "translations", "frontend", filename)
    path_backend_file  = os.path.join(dir_path, "apps", "nspanel-lovelace-ui", "luibackend", "translations", "backend" , filename)
    return path_frontend_file, path_backend_file

def lookup(path_frontend_file, path_backend_file, lookupstr):
    with open(path_frontend_file, 'r', encoding="utf-8") as f, open(path_backend_file, 'r', encoding="utf-8") as b:
        translations = { "frontend": json.load(f), "backend": json.load(b)}
        res = translations
        for k in lookupstr.split("."):
            if k in res:
                res = res[k]
        if type(res) is not str:
            print("Warning result is not a String")
        return res

def get_translation(locale, lookupstr):
    path_frontend_file, path_backend_file = build_locale_filestring(locale)
    res = lookup(path_frontend_file, path_backend_file, lookupstr)
    return res
    
out = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
for src, dst in keys.items():
    dst = dst.split(".")
    for lang in langs:
        out[dst[0]][dst[1]][lang] = get_translation(lang, src)

#print(json.dumps(out, indent=4, ensure_ascii=False))

with open("ioBroker_NSPanel_locales.json", "wb") as text_file:
    text_file.write(json.dumps(out, indent=4, ensure_ascii=False).encode('utf8'))