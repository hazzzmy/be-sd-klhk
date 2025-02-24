from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi import FastAPI, HTTPException, Security, Response, Depends, Request,File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List

import logging
from pydantic import BaseModel, ValidationError

import pysd
import traceback
import json
import warnings
import shutil
warnings.filterwarnings("ignore")
import os



import uvicorn
from enum import Enum

app = FastAPI(docs_url=None, redoc_url=None, title="KLHK Systemdynamic API", version="1.0.0")

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:3000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


logging.basicConfig(level=logging.INFO)

@app.get("/")
async def root():
    return {"message": "KLHK Systemdynamic API is Running"}

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="https://unpkg.com/redoc@next/bundles/redoc.standalone.js",
    )


class Parameter(BaseModel):
    island:str
    # parameter:List[str]
    simulation:str = 'baseline'
    initial_time: int = 2016
    final_time: int = 2055
    mps_assumption: float = 0.36
    time_to_change_mps_assumption:int = 3000
    laju_pertumbuhan_populasi_asumsi: float = 0.0116116
    time_to_change_laju_pertumbuhan_populasi_asumsi: int = 3000
    laju_perubahan_lahan_terbangun_per_kapita_asumsi: float = 0.03
    time_to_change_laju_perubahan_lahan_terbangun_per_kapita:int = 3000
    elastisitas_lpe_thd_perubahan_teknologi_target: float = 0.35
    time_to_change_elastisitas_lpe_thd_perubahan_teknologi : int = 3000
    std_kebutuhan_air_per_kapita_sk_146_2023_target: float = 42.3
    waktu_pengubahan_standar_kebutuhan_air_per_kapita: int = 3000
    debit_per_detik_pertanian_dasar_sk_146_2023_skenario: float = 1
    waktu_perubahan_std_debit_per_detik_pertanian:int = 3000
    lahan_pangan_per_kapita_skenario:int = 740
    waktu_perubahan_lahan_pangan_per_kapita:int = 3000
    lahan_built_up_per_kapita_skenario:int = 20
    waktu_perubahan_lahan_built_up_per_kapita:int = 3000


@app.post('/postSystemDynamic', status_code=201)
async def handle_get_sd(parameter:Parameter):

    try:

        inputModel = pysd.load(f"./data/production/model_{parameter.island}.py")

        model = inputModel.run(initial_condition=(parameter.initial_time,{}), final_time=parameter.final_time)

        with open("param.txt", "w") as file:
            for item in model.columns:
                file.write(f"{item}\n")
        
        # if len(parameter.parameter) > 0:
        #     model = model[parameter.parameter]

        model['time'] = model.index
        time_col = model.pop('time')
        model.insert(0, 'time', time_col)
        
        model_json = json.loads(model.to_json(orient="records"))
        if parameter.simulation != 'baseline':
            inputModel.set_components({
                'mps assumption': parameter.mps_assumption,
                'time to change mps assumption': parameter.time_to_change_mps_assumption,
                'laju pertumbuhan populasi asumsi': parameter.laju_pertumbuhan_populasi_asumsi,
                'time to change laju pertumbuhan populasi asumsi': parameter.time_to_change_laju_pertumbuhan_populasi_asumsi,
                'laju perubahan lahan terbangun per kapita asumsi': parameter.laju_perubahan_lahan_terbangun_per_kapita_asumsi,
                'time to change laju perubahan lahan terbangun per kapita': parameter.time_to_change_laju_perubahan_lahan_terbangun_per_kapita,
                'Elastisitas LPE thd perubahan teknologi target':parameter.elastisitas_lpe_thd_perubahan_teknologi_target,
                'time to change Elastisitas LPE thd perubahan teknologi': parameter.time_to_change_elastisitas_lpe_thd_perubahan_teknologi,
                '"std kebutuhan air per kapita SK 146/2023 target"': parameter.std_kebutuhan_air_per_kapita_sk_146_2023_target,
                'Waktu pengubahan standard air': parameter.waktu_pengubahan_standar_kebutuhan_air_per_kapita,
                '"debit per detik pertanian dasar SK 146/2023 skenario"': parameter.debit_per_detik_pertanian_dasar_sk_146_2023_skenario,
                'Waktu perubahan std debit per detik pertanian': parameter.waktu_perubahan_std_debit_per_detik_pertanian,
                'Lahan Pangan Per Kapita Skenario': parameter.lahan_pangan_per_kapita_skenario,
                'Waktu perubahan lahan pangan per kapita': parameter.waktu_perubahan_lahan_pangan_per_kapita,
                '"Lahan built-up per kapita skenario"': parameter.lahan_built_up_per_kapita_skenario,
                '"Waktu perubahan Lahan built-up per kapita"': parameter.waktu_perubahan_lahan_built_up_per_kapita,
            })
        
        sim_moodel = inputModel.run(initial_condition=(parameter.initial_time, {}), final_time=parameter.final_time,cache_output=True)
        
        # if len(parameter.parameter) > 0:
        #     sim_moodel = sim_moodel[parameter.parameter]

        sim_moodel['time'] = sim_moodel.index
        time_col = sim_moodel.pop('time')
        sim_moodel.insert(0, 'time', time_col)
        
        sim_moodel_json = json.loads(sim_moodel.to_json(orient="records"))

        return {
            "island": parameter.island,
            "simulation": parameter.simulation,
            "baseline": model_json,
            "result": sim_moodel_json
        }
        
        

    except ValidationError as e:
        return {'Validation Error': e}

    except Exception as e:
        tb_str = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
        raise HTTPException(status_code=500, detail=f'ERROR: {e}\n{tb_str}')
    

# Enum for dropdown options
class IslandEnum(str, Enum):
    sumatera = "sumatera"
    jawa = "jawa"
    balinusra = "balinusra"
    kalimantan = "kalimantan"
    sulawesi = "sulawesi"
    maluku = "maluku"
    papua = "papua"

@app.post("/upload-sd-model")
async def upload(
    file: UploadFile = File(...),
    island: IslandEnum = Form(...)
):
    try:
        # file_bytes = await file.read()
        file_path = f'model_{island.value}.mdl'

        parameter = {
            "island": "sumatera",
            "parameter": [
                "string"
            ],
            "simulation": "baseline",
            "initial_time": 2016,
            "final_time": 2055,
            "mps_assumption": 0.36,
            "time_to_change_mps_assumption": 3000,
            "laju_pertumbuhan_populasi_asumsi": 0.0116116,
            "time_to_change_laju_pertumbuhan_populasi_asumsi": 3000,
            "laju_perubahan_lahan_terbangun_per_kapita_asumsi": 0.03,
            "time_to_change_laju_perubahan_lahan_terbangun_per_kapita": 3000,
            "elastisitas_lpe_thd_perubahan_teknologi_target": 0.35,
            "time_to_change_elastisitas_lpe_thd_perubahan_teknologi": 3000,
            "std_kebutuhan_air_per_kapita_sk_146_2023_target": 42.3,
            "waktu_pengubahan_standar_kebutuhan_air_per_kapita": 3000,
            "debit_per_detik_pertanian_dasar_sk_146_2023_skenario":  1,
            "waktu_perubahan_std_debit_per_detik_pertanian":3000,
            "lahan_pangan_per_kapita_skenario":740,
            "waktu_perubahan_lahan_pangan_per_kapita":3000,
            "lahan_built_up_per_kapita_skenario":20,
            "waktu_perubahan_lahan_built_up_per_kapita":3000
        }
        
        with open(file_path, "wb") as f:
             f.write(await file.read())

        inputModel = pysd.read_vensim(file_path)
        model = inputModel.run(initial_condition=(parameter["initial_time"],{}), final_time=parameter["final_time"])
        
        source =  f'model_{island.value}.py'
        destination = f'./data/production/model_{island.value}.py'

        os.rename(source, destination)

        return {
            "message": "Converting Completed",
            "island": island
        }

    except Exception as e:
        tb_str = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}\n{tb_str}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
