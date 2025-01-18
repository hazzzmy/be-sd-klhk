"""
Python model 'model_maluku.py'
Translated using PySD
"""

from pathlib import Path
import numpy as np

from pysd.py_backend.functions import step
from pysd.py_backend.statefuls import Trend, Initial, Delay, Integ, Smooth
from pysd.py_backend.lookups import HardcodedLookups
from pysd import Component

__pysd_version__ = "3.14.1"

__data = {"scope": None, "time": lambda: 0}

_root = Path(__file__).parent


component = Component()

#######################################################################
#                          CONTROL VARIABLES                          #
#######################################################################

_control_vars = {
    "initial_time": lambda: 2016,
    "final_time": lambda: 2055,
    "time_step": lambda: 0.125,
    "saveper": lambda: 1,
}


def _init_outer_references(data):
    for key in data:
        __data[key] = data[key]


@component.add(name="Time")
def time():
    """
    Current time of the model.
    """
    return __data["time"]()


@component.add(
    name="FINAL TIME", units="tahun", comp_type="Constant", comp_subtype="Normal"
)
def final_time():
    """
    The final time for the simulation.
    """
    return __data["time"].final_time()


@component.add(
    name="INITIAL TIME", units="tahun", comp_type="Constant", comp_subtype="Normal"
)
def initial_time():
    """
    The initial time for the simulation.
    """
    return __data["time"].initial_time()


@component.add(
    name="SAVEPER",
    units="tahun",
    limits=(0.0, np.nan),
    comp_type="Constant",
    comp_subtype="Normal",
)
def saveper():
    """
    The frequency with which output is stored.
    """
    return __data["time"].saveper()


@component.add(
    name="TIME STEP",
    units="tahun",
    limits=(0.0, np.nan),
    comp_type="Constant",
    comp_subtype="Normal",
)
def time_step():
    """
    The time step for the simulation.
    """
    return __data["time"].time_step()


#######################################################################
#                           MODEL VARIABLES                           #
#######################################################################


@component.add(
    name="Laju Perubahan Lahan Terbangun per Kapita historis and policy",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "perubahan_laju_perubahan_lahan_terbangun_per_kapita_delay": 1,
        "laju_perubahan_lahan_terbangun_per_kapita": 1,
    },
)
def laju_perubahan_lahan_terbangun_per_kapita_historis_and_policy():
    return (
        perubahan_laju_perubahan_lahan_terbangun_per_kapita_delay()
        + laju_perubahan_lahan_terbangun_per_kapita()
    )


@component.add(
    name="Laju Perubahan Lahan Terbangun per Kapita asumsi",
    units="1/tahun",
    comp_type="Constant",
    comp_subtype="Normal",
)
def laju_perubahan_lahan_terbangun_per_kapita_asumsi():
    return 0.01


@component.add(
    name="perubahan Laju Perubahan Lahan Terbangun per Kapita",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "laju_perubahan_lahan_terbangun_per_kapita_asumsi": 1,
        "laju_perubahan_lahan_terbangun_per_kapita": 1,
        "time_to_change_laju_perubahan_lahan_terbangun_per_kapita": 1,
        "time": 1,
    },
)
def perubahan_laju_perubahan_lahan_terbangun_per_kapita():
    return step(
        __data["time"],
        laju_perubahan_lahan_terbangun_per_kapita_asumsi()
        - laju_perubahan_lahan_terbangun_per_kapita(),
        time_to_change_laju_perubahan_lahan_terbangun_per_kapita(),
    )


@component.add(
    name="Perubahan Lahan Terbangun per Kapita",
    units="Ha/(tahun*jiwa)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "laju_perubahan_lahan_terbangun_per_kapita_historis_and_policy": 1,
        "lahan_terbangun_per_kapita": 1,
    },
)
def perubahan_lahan_terbangun_per_kapita():
    return (
        laju_perubahan_lahan_terbangun_per_kapita_historis_and_policy()
        * lahan_terbangun_per_kapita()
    )


@component.add(
    name="time to change Laju Perubahan Lahan Terbangun per Kapita",
    units="tahun",
    comp_type="Constant",
    comp_subtype="Normal",
)
def time_to_change_laju_perubahan_lahan_terbangun_per_kapita():
    return 3000


@component.add(
    name="delay on perubahan Laju Perubahan Lahan Terbangun per Kapita",
    units="tahun",
    comp_type="Constant",
    comp_subtype="Normal",
)
def delay_on_perubahan_laju_perubahan_lahan_terbangun_per_kapita():
    return 5


@component.add(
    name="perubahan Laju Perubahan Lahan Terbangun per Kapita delay",
    units="Dmnl/tahun",
    comp_type="Stateful",
    comp_subtype="Delay",
    depends_on={"_delay_perubahan_laju_perubahan_lahan_terbangun_per_kapita_delay": 1},
    other_deps={
        "_delay_perubahan_laju_perubahan_lahan_terbangun_per_kapita_delay": {
            "initial": {
                "delay_on_perubahan_laju_perubahan_lahan_terbangun_per_kapita": 1
            },
            "step": {
                "perubahan_laju_perubahan_lahan_terbangun_per_kapita": 1,
                "delay_on_perubahan_laju_perubahan_lahan_terbangun_per_kapita": 1,
            },
        }
    },
)
def perubahan_laju_perubahan_lahan_terbangun_per_kapita_delay():
    return _delay_perubahan_laju_perubahan_lahan_terbangun_per_kapita_delay()


_delay_perubahan_laju_perubahan_lahan_terbangun_per_kapita_delay = Delay(
    lambda: perubahan_laju_perubahan_lahan_terbangun_per_kapita(),
    lambda: delay_on_perubahan_laju_perubahan_lahan_terbangun_per_kapita(),
    lambda: 0,
    lambda: 3,
    time_step,
    "_delay_perubahan_laju_perubahan_lahan_terbangun_per_kapita_delay",
)


@component.add(
    name="Tabungan",
    units="JutaRp/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"mps_historical_and_policy": 1, "pendapatan_untuk_digunakan": 1},
)
def tabungan():
    return mps_historical_and_policy() * pendapatan_untuk_digunakan()


@component.add(
    name="perubahan Elastisitas LPE thd perubahan teknologi delay",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Delay",
    depends_on={"_delay_perubahan_elastisitas_lpe_thd_perubahan_teknologi_delay": 1},
    other_deps={
        "_delay_perubahan_elastisitas_lpe_thd_perubahan_teknologi_delay": {
            "initial": {"delay_on_change_elastisitas_lpe_thd_perubahan_teknologi": 1},
            "step": {
                "perubahan_elastisitas_lpe_thd_perubahan_teknologi": 1,
                "delay_on_change_elastisitas_lpe_thd_perubahan_teknologi": 1,
            },
        }
    },
)
def perubahan_elastisitas_lpe_thd_perubahan_teknologi_delay():
    return _delay_perubahan_elastisitas_lpe_thd_perubahan_teknologi_delay()


_delay_perubahan_elastisitas_lpe_thd_perubahan_teknologi_delay = Delay(
    lambda: perubahan_elastisitas_lpe_thd_perubahan_teknologi(),
    lambda: delay_on_change_elastisitas_lpe_thd_perubahan_teknologi(),
    lambda: 0,
    lambda: 3,
    time_step,
    "_delay_perubahan_elastisitas_lpe_thd_perubahan_teknologi_delay",
)


@component.add(
    name="Perubahan tk teknologi",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "lpe_pulau": 1,
        "elastisitas_lpe_thd_perubahan_teknologi": 1,
        "tingkat_teknologi": 1,
    },
)
def perubahan_tk_teknologi():
    return lpe_pulau() * elastisitas_lpe_thd_perubahan_teknologi() * tingkat_teknologi()


@component.add(
    name="delay on change Elastisitas LPE thd perubahan teknologi",
    units="tahun",
    comp_type="Constant",
    comp_subtype="Normal",
)
def delay_on_change_elastisitas_lpe_thd_perubahan_teknologi():
    return 5


@component.add(
    name="delay on mps change assumption",
    units="tahun",
    comp_type="Constant",
    comp_subtype="Normal",
)
def delay_on_mps_change_assumption():
    return 5


@component.add(
    name="delay on perubahan laju pertumbuhan populasi",
    units="tahun",
    comp_type="Constant",
    comp_subtype="Normal",
)
def delay_on_perubahan_laju_pertumbuhan_populasi():
    return 5


@component.add(
    name="mps change delay",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Delay",
    depends_on={"_delay_mps_change_delay": 1},
    other_deps={
        "_delay_mps_change_delay": {
            "initial": {"delay_on_mps_change_assumption": 1},
            "step": {"mps_change": 1, "delay_on_mps_change_assumption": 1},
        }
    },
)
def mps_change_delay():
    return _delay_mps_change_delay()


_delay_mps_change_delay = Delay(
    lambda: mps_change(),
    lambda: delay_on_mps_change_assumption(),
    lambda: 0,
    lambda: 3,
    time_step,
    "_delay_mps_change_delay",
)


@component.add(
    name="Pertumbuhan populasi",
    units="jiwa/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"populasi_pulau": 1, "lpp_historis_dan_policy": 1},
)
def pertumbuhan_populasi():
    return populasi_pulau() * lpp_historis_dan_policy()


@component.add(
    name="perubahan Elastisitas LPE thd perubahan teknologi",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "elastisitas_lpe_thd_perubahan_teknologi_target": 1,
        "elastisitas_lpe_thd_perubahan_teknologi_historis": 1,
        "time_to_change_elastisitas_lpe_thd_perubahan_teknologi": 1,
        "time": 1,
    },
)
def perubahan_elastisitas_lpe_thd_perubahan_teknologi():
    return step(
        __data["time"],
        elastisitas_lpe_thd_perubahan_teknologi_target()
        - elastisitas_lpe_thd_perubahan_teknologi_historis(),
        time_to_change_elastisitas_lpe_thd_perubahan_teknologi(),
    )


@component.add(
    name="Elastisitas LPE thd perubahan teknologi",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "elastisitas_lpe_thd_perubahan_teknologi_historis": 1,
        "perubahan_elastisitas_lpe_thd_perubahan_teknologi_delay": 1,
    },
)
def elastisitas_lpe_thd_perubahan_teknologi():
    return (
        elastisitas_lpe_thd_perubahan_teknologi_historis()
        + perubahan_elastisitas_lpe_thd_perubahan_teknologi_delay()
    )


@component.add(
    name="time to change laju pertumbuhan populasi asumsi",
    units="tahun",
    comp_type="Constant",
    comp_subtype="Normal",
)
def time_to_change_laju_pertumbuhan_populasi_asumsi():
    return 3000


@component.add(
    name="time to change mps assumption",
    units="tahun",
    comp_type="Constant",
    comp_subtype="Normal",
)
def time_to_change_mps_assumption():
    return 3000


@component.add(
    name="laju pertumbuhan populasi asumsi",
    units="1/tahun",
    comp_type="Constant",
    comp_subtype="Normal",
)
def laju_pertumbuhan_populasi_asumsi():
    return 0.0196


@component.add(
    name="perubahan laju pertumbuhan populasi",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "laju_pertumbuhan_populasi_asumsi": 1,
        "laju_pertumbuhan_populasi": 1,
        "time_to_change_laju_pertumbuhan_populasi_asumsi": 1,
        "time": 1,
    },
)
def perubahan_laju_pertumbuhan_populasi():
    return step(
        __data["time"],
        laju_pertumbuhan_populasi_asumsi() - laju_pertumbuhan_populasi(),
        time_to_change_laju_pertumbuhan_populasi_asumsi(),
    )


@component.add(
    name="perubahan laju pertumbuhan populasi delay",
    units="Dmnl/tahun",
    comp_type="Stateful",
    comp_subtype="Delay",
    depends_on={"_delay_perubahan_laju_pertumbuhan_populasi_delay": 1},
    other_deps={
        "_delay_perubahan_laju_pertumbuhan_populasi_delay": {
            "initial": {"delay_on_perubahan_laju_pertumbuhan_populasi": 1},
            "step": {
                "perubahan_laju_pertumbuhan_populasi": 1,
                "delay_on_perubahan_laju_pertumbuhan_populasi": 1,
            },
        }
    },
)
def perubahan_laju_pertumbuhan_populasi_delay():
    return _delay_perubahan_laju_pertumbuhan_populasi_delay()


_delay_perubahan_laju_pertumbuhan_populasi_delay = Delay(
    lambda: perubahan_laju_pertumbuhan_populasi(),
    lambda: delay_on_perubahan_laju_pertumbuhan_populasi(),
    lambda: 0,
    lambda: 3,
    time_step,
    "_delay_perubahan_laju_pertumbuhan_populasi_delay",
)


@component.add(
    name="Elastisitas LPE thd perubahan teknologi target",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def elastisitas_lpe_thd_perubahan_teknologi_target():
    return 0.37


@component.add(
    name="LPP historis dan policy",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "laju_pertumbuhan_populasi": 1,
        "perubahan_laju_pertumbuhan_populasi_delay": 1,
    },
)
def lpp_historis_dan_policy():
    return laju_pertumbuhan_populasi() + perubahan_laju_pertumbuhan_populasi_delay()


@component.add(
    name="mps historical and policy",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"mps": 1, "mps_change_delay": 1},
)
def mps_historical_and_policy():
    return mps() + mps_change_delay()


@component.add(
    name="time to change Elastisitas LPE thd perubahan teknologi",
    units="tahun",
    comp_type="Constant",
    comp_subtype="Normal",
)
def time_to_change_elastisitas_lpe_thd_perubahan_teknologi():
    return 3000


@component.add(
    name="mps assumption", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def mps_assumption():
    return 0.32


@component.add(
    name="mps change",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "mps_assumption": 1,
        "mps": 1,
        "time_to_change_mps_assumption": 1,
        "time": 1,
    },
)
def mps_change():
    return step(
        __data["time"], mps_assumption() - mps(), time_to_change_mps_assumption()
    )


@component.add(
    name="Ambang Batas populasi Air",
    units="jiwa",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_ketersediaan_air_bisa_digunakan": 1,
        "std_kebutuhan_air_per_kapita_kebutuhan_sk_1462023": 1,
    },
)
def ambang_batas_populasi_air():
    return (
        total_ketersediaan_air_bisa_digunakan()
        / std_kebutuhan_air_per_kapita_kebutuhan_sk_1462023()
    )


@component.add(
    name="Fraksi lahan pangan dimanfaatkan",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def fraksi_lahan_pangan_dimanfaatkan():
    return 0.562613


@component.add(
    name="Indeks D3T Air",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"rasio_kecukupan_air_sk_146": 1},
)
def indeks_d3t_air():
    return 1 / rasio_kecukupan_air_sk_146()


@component.add(
    name='"std kebutuhan air per kapita kebutuhan SK 146/2023"',
    units="m*m*m/(jiwa*tahun)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def std_kebutuhan_air_per_kapita_kebutuhan_sk_1462023():
    return 850


@component.add(
    name="Kebutuhan lahan",
    units="Ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"populasi_pulau": 1, "kebutuhan_lahan_per_orang": 1},
)
def kebutuhan_lahan():
    return populasi_pulau() * kebutuhan_lahan_per_orang()


@component.add(
    name="Kebutuhan lahan per orang",
    units="Ha/jiwa",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"lahan_builtup_per_kapita": 1, "lahan_pangan_per_kapita": 1},
)
def kebutuhan_lahan_per_orang():
    return lahan_builtup_per_kapita() + lahan_pangan_per_kapita()


@component.add(
    name="Indeks D3T Lahan",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"biokapasitas_pangan": 1, "kebutuhan_lahan": 1},
)
def indeks_d3t_lahan():
    return biokapasitas_pangan() / kebutuhan_lahan()


@component.add(
    name="Ambang Batas populasi dari Lahan",
    units="jiwa",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"biokapasitas_pangan": 1, "kebutuhan_lahan_per_orang": 1},
)
def ambang_batas_populasi_dari_lahan():
    return biokapasitas_pangan() / kebutuhan_lahan_per_orang()


@component.add(
    name="Biokapasitas Pangan",
    units="Ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_lahan": 1,
        "pertambangan": 1,
        "lahan_terbangun": 1,
        "lahan_lainnya": 1,
        "fraksi_lahan_pangan_dimanfaatkan": 1,
    },
)
def biokapasitas_pangan():
    return (
        total_lahan() - pertambangan() - lahan_terbangun() - lahan_lainnya()
    ) * fraksi_lahan_pangan_dimanfaatkan()


@component.add(
    name="Lahan Terbangun per Kapita",
    units="Ha/jiwa",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_lahan_terbangun_per_kapita": 1},
    other_deps={
        "_integ_lahan_terbangun_per_kapita": {
            "initial": {"lahan_terbangun_per_kapita_init": 1, "mult": 1},
            "step": {"perubahan_lahan_terbangun_per_kapita": 1},
        }
    },
)
def lahan_terbangun_per_kapita():
    return _integ_lahan_terbangun_per_kapita()


_integ_lahan_terbangun_per_kapita = Integ(
    lambda: perubahan_lahan_terbangun_per_kapita(),
    lambda: lahan_terbangun_per_kapita_init() * mult(),
    "_integ_lahan_terbangun_per_kapita",
)


@component.add(
    name="kebutuhan air pertanian SK 146",
    units="m*m*m/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pertanian": 1,
        "std_kebutuhan_air_per_pertanian_sk_1462023_tahunan": 1,
        "koefisien_i_persawahan": 1,
    },
)
def kebutuhan_air_pertanian_sk_146():
    return (
        pertanian()
        * std_kebutuhan_air_per_pertanian_sk_1462023_tahunan()
        * koefisien_i_persawahan()
    )


@component.add(
    name="Total ketersediaan air",
    units="m*m*m/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "potensi_air_tanah": 1,
        "aktivasi_potensi_air_tanah": 1,
        "supply_air_permukaan": 1,
    },
)
def total_ketersediaan_air():
    return potensi_air_tanah() * aktivasi_potensi_air_tanah() + supply_air_permukaan()


@component.add(
    name="aktivasi potensi air tanah",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def aktivasi_potensi_air_tanah():
    return 0


@component.add(
    name="Biokapasitas tempat tinggal",
    units="Ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"lahan_terbangun": 1},
)
def biokapasitas_tempat_tinggal():
    return lahan_terbangun()


@component.add(
    name='"Lahan Built-up per kapita"',
    units="Ha/jiwa",
    comp_type="Constant",
    comp_subtype="Normal",
)
def lahan_builtup_per_kapita():
    return 0.0024956


@component.add(
    name="jejak ekologis tempat tinggal",
    units="Ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"lahan_builtup_per_kapita": 1, "populasi_pulau": 1},
)
def jejak_ekologis_tempat_tinggal():
    return lahan_builtup_per_kapita() * populasi_pulau()


@component.add(
    name="Ambang batas penduduk tempat tinggal",
    units="jiwa",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"biokapasitas_tempat_tinggal": 1, "lahan_builtup_per_kapita": 1},
)
def ambang_batas_penduduk_tempat_tinggal():
    return biokapasitas_tempat_tinggal() / lahan_builtup_per_kapita()


@component.add(
    name='"faktor koreksi kebutuhan air per kap SK 146/2023"',
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def faktor_koreksi_kebutuhan_air_per_kap_sk_1462023():
    return 2


@component.add(
    name="Total kebutuhan air SK 146",
    units="m*m*m/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"kebutuhan_air_domestik_sk_146": 1, "kebutuhan_air_ekonomi": 1},
)
def total_kebutuhan_air_sk_146():
    return kebutuhan_air_domestik_sk_146() + kebutuhan_air_ekonomi()


@component.add(
    name="koefisien I persawahan",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def koefisien_i_persawahan():
    return 4


@component.add(
    name="koefisien I pertanian lahan kering",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def koefisien_i_pertanian_lahan_kering():
    return 1.5


@component.add(
    name='"std kebutuhan air per perkebunan SK 146/2023 tahunan"',
    units="m*m*m/(Ha*tahun)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "koefisien_i_perkebunan": 1,
        "std_kebutuhan_air_per_pertanian_sk_1462023_tahunan": 1,
    },
)
def std_kebutuhan_air_per_perkebunan_sk_1462023_tahunan():
    return (
        koefisien_i_perkebunan() * std_kebutuhan_air_per_pertanian_sk_1462023_tahunan()
    )


@component.add(
    name="koefisien I perkebunan",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def koefisien_i_perkebunan():
    return 1.5


@component.add(
    name="koefisien I pertanian lahan kering campur",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def koefisien_i_pertanian_lahan_kering_campur():
    return 1


@component.add(
    name="Rasio kecukupan lahan tempat tinggal",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"biokapasitas_tempat_tinggal": 1, "jejak_ekologis_tempat_tinggal": 1},
)
def rasio_kecukupan_lahan_tempat_tinggal():
    return biokapasitas_tempat_tinggal() / jejak_ekologis_tempat_tinggal()


@component.add(
    name="Kebutuhan air ekonomi",
    units="m*m*m/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "kebutuhan_air_perkebunan_sk_146": 1,
        "kebutuhan_air_pertanian_sk_146": 1,
    },
)
def kebutuhan_air_ekonomi():
    """
    kalibrasi dengan laporan
    """
    return (
        kebutuhan_air_perkebunan_sk_146() + kebutuhan_air_pertanian_sk_146()
    ) * 0.275379


@component.add(
    name="kebutuhan air domestik SK 146",
    units="m*m*m/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "std_kebutuhan_air_per_kapita_sk_1462023": 1,
        "populasi_pulau": 1,
        "faktor_koreksi_kebutuhan_air_per_kap_sk_1462023": 1,
    },
)
def kebutuhan_air_domestik_sk_146():
    return (
        std_kebutuhan_air_per_kapita_sk_1462023()
        * populasi_pulau()
        * faktor_koreksi_kebutuhan_air_per_kap_sk_1462023()
    )


@component.add(
    name="PDRB Pulau",
    units="JutaRp/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pdrb_pulau_awal": 1,
        "kapital_awal": 1,
        "intensitas_kapital": 2,
        "kapital": 1,
        "tenaga_kerja": 1,
        "tenaga_kerja_awal": 1,
        "tingkat_teknologi": 1,
        "capacity_utilization_factor": 1,
        "dampak_kecukupan_air_industri_ekonomi": 1,
        "dampak_kualitas_air_industri_ekonomi_delay": 1,
    },
)
def pdrb_pulau():
    return (
        pdrb_pulau_awal()
        * (kapital() / kapital_awal()) ** intensitas_kapital()
        * (tenaga_kerja() / tenaga_kerja_awal()) ** (1 - intensitas_kapital())
        * tingkat_teknologi()
        * capacity_utilization_factor()
        * dampak_kecukupan_air_industri_ekonomi()
        * dampak_kualitas_air_industri_ekonomi_delay()
    )


@component.add(
    name='"Rawa & Badan Air ke Lahan Terbangun"',
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "availability_effect_rawa_badan_air": 1,
        "rawa_badan_air_ke_lahan_terbangun_indicated": 1,
    },
)
def rawa_badan_air_ke_lahan_terbangun():
    return (
        availability_effect_rawa_badan_air()
        * rawa_badan_air_ke_lahan_terbangun_indicated()
    )


@component.add(
    name="Pertanian to Lahan Terbangun",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "availability_effect_pertanian": 1,
        "pertanian_to_lahan_terbangun_indicated": 1,
    },
)
def pertanian_to_lahan_terbangun():
    return availability_effect_pertanian() * pertanian_to_lahan_terbangun_indicated()


@component.add(
    name="Belukar Padang Rumput to Lahan Terbangun",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "availability_effect_belukar_padang_rumput": 1,
        "belukar_padang_rumput_to_lahan_terbangun_indicated": 1,
    },
)
def belukar_padang_rumput_to_lahan_terbangun():
    return (
        availability_effect_belukar_padang_rumput()
        * belukar_padang_rumput_to_lahan_terbangun_indicated()
    )


@component.add(
    name="Lahan Lainnya ke Lahan Terbangun",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "availability_effect_lahan_lainnya": 1,
        "lahan_lainnya_ke_lahan_terbangun_indicated": 1,
    },
)
def lahan_lainnya_ke_lahan_terbangun():
    return (
        availability_effect_lahan_lainnya()
        * lahan_lainnya_ke_lahan_terbangun_indicated()
    )


@component.add(
    name="Hutan Mangrove to Lahan Terbangun",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "availability_effect_hutan_mangrove": 1,
        "hutan_mangrove_to_lahan_terbangun_indicated": 1,
    },
)
def hutan_mangrove_to_lahan_terbangun():
    return (
        availability_effect_hutan_mangrove()
        * hutan_mangrove_to_lahan_terbangun_indicated()
    )


@component.add(
    name="Pertambangan ke Lahan Terbangun",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "availability_effect_pertambangan": 1,
        "pertambangan_ke_lahan_terbangun_indicated": 1,
    },
)
def pertambangan_ke_lahan_terbangun():
    return (
        availability_effect_pertambangan() * pertambangan_ke_lahan_terbangun_indicated()
    )


@component.add(
    name="Perkebunan to Lahan Terbangun",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "availability_effect_perkebunan": 1,
        "perkebunan_to_lahan_terbangun_indicated": 1,
    },
)
def perkebunan_to_lahan_terbangun():
    return availability_effect_perkebunan() * perkebunan_to_lahan_terbangun_indicated()


@component.add(
    name="Hutan Tanaman to Lahan Terbangun",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "availability_effect_hutan_tanaman": 1,
        "hutan_tanaman_to_lahan_terbangun_indicated": 1,
    },
)
def hutan_tanaman_to_lahan_terbangun():
    return (
        availability_effect_hutan_tanaman()
        * hutan_tanaman_to_lahan_terbangun_indicated()
    )


@component.add(
    name='"Hutan Primer & Hutan Sekunder to Lahan Terbangun"',
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "availability_effect_hutan_primer_sekunder": 1,
        "hutan_primer_hutan_sekunder_to_lahan_terbangun_indicated": 1,
    },
)
def hutan_primer_hutan_sekunder_to_lahan_terbangun():
    return (
        availability_effect_hutan_primer_sekunder()
        * hutan_primer_hutan_sekunder_to_lahan_terbangun_indicated()
    )


@component.add(
    name="Lahan Terbangun to Hutan Mangrove share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def lahan_terbangun_to_hutan_mangrove_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [4.56e-03, 1.63e-05, 1.05e-03, 0.00e00, 1.35e-03, 0.00e00, 1.16e-03],
    )


@component.add(
    name='"Lahan Terbangun to Hutan Primer & Sekunder share"',
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def lahan_terbangun_to_hutan_primer_sekunder_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [3.70e-04, 1.77e-05, 4.94e-03, 0.00e00, 2.79e-03, 0.00e00, 1.35e-03],
    )


@component.add(
    name='"Hutan Primer & Sekunder ke Lahan Lainnya share"',
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def hutan_primer_sekunder_ke_lahan_lainnya_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [7.56e-04, 1.03e-06, 2.54e-04, 1.93e-03, 9.36e-04, 3.56e-04, 7.06e-04],
    )


@component.add(
    name='"Hutan Primer & Sekunder ke Pertambangan share"',
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def hutan_primer_sekunder_ke_pertambangan_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [7.88e-08, 7.24e-05, 3.25e-05, 2.29e-05, 1.26e-04, 5.38e-05, 5.13e-05],
    )


@component.add(
    name="Lahan Terbangun to Hutan Tanaman share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def lahan_terbangun_to_hutan_tanaman_share():
    return np.interp(
        time_index(), [2016, 2017, 2018, 2019, 2020, 2021, 2022], [0, 0, 0, 0, 0, 0, 0]
    )


@component.add(
    name="Belukar Padang Rumput to Hutan Tanaman share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def belukar_padang_rumput_to_hutan_tanaman_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [0.00e00, 6.72e-11, 8.23e-14, 0.00e00, 7.63e-04, 0.00e00, 1.27e-04],
    )


@component.add(
    name="Pertanian to Perkebunan share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def pertanian_to_perkebunan_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [0.00178, 0.0, 0.00185, 0.0, 0.000152, 0.0, 0.00063],
    )


@component.add(
    name='"Hutan Primer & Sekunder to Belukar Padang Rumput share"',
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def hutan_primer_sekunder_to_belukar_padang_rumput_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [7.05e-03, 1.03e-03, 3.21e-03, 7.30e-05, 5.25e-03, 3.79e-04, 2.83e-03],
    )


@component.add(
    name="Lahan Terbangun to Perkebunan share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def lahan_terbangun_to_perkebunan_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [0.000595, 0.0, 0.00185, 0.0, 0.00259, 0.0, 0.000839],
    )


@component.add(
    name='"Hutan Primer & Sekunder to Hutan Tanaman share"',
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def hutan_primer_sekunder_to_hutan_tanaman_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [5.97e-07, 2.76e-11, 1.24e-11, 0.00e00, 8.12e-06, 0.00e00, 1.45e-06],
    )


@component.add(
    name='"Hutan Primer & Sekunder to Lahan Terbangun share"',
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def hutan_primer_sekunder_to_lahan_terbangun_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [1.45e-04, 6.03e-06, 8.02e-05, 0.00e00, 7.62e-05, 2.41e-06, 5.16e-05],
    )


@component.add(
    name='"Hutan Primer & Sekunder to Perkebunan share"',
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def hutan_primer_sekunder_to_perkebunan_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [2.54e-05, 0.00e00, 3.63e-04, 0.00e00, 1.26e-05, 0.00e00, 6.68e-05],
    )


@component.add(
    name="Lahan Terbangun to Pertanian share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def lahan_terbangun_to_pertanian_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [0.0909, 0.119, 0.0316, 0.000434, 0.0709, 0.0, 0.0521],
    )


@component.add(
    name="Belukar Padang Rumput to Perkebunan share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def belukar_padang_rumput_to_perkebunan_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [0.000884, 0.00098, 0.00293, 0.0, 0.000302, 0.0, 0.000849],
    )


@component.add(
    name="Pertanian Hist",
    units="Ha",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def pertanian_hist():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [1525140.0, 1469870.0, 1487260.0, 1416560.0, 1414700.0, 1413880.0, 1413270.0],
    )


@component.add(
    name="Hutan Tanaman Hist",
    units="Ha",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def hutan_tanaman_hist():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [36986.0, 36967.8, 36823.8, 36647.6, 36647.6, 38179.5, 38179.5],
    )


@component.add(
    name="Belukar Padang Rumput to Pertanian share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def belukar_padang_rumput_to_pertanian_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [0.0211, 0.00975, 0.0328, 0.0012, 0.0333, 0.000378, 0.0164],
    )


@component.add(
    name="Pertambangan Hist",
    units="Ha",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def pertambangan_hist():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [4059.52, 4101.66, 4225.95, 6654.05, 7739.52, 9389.07, 10100.6],
    )


@component.add(
    name="Hutan Tanaman ke Lahan Lainnya share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def hutan_tanaman_ke_lahan_lainnya_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [0.00e00, 6.48e-10, 0.00e00, 0.00e00, 0.00e00, 0.00e00, 1.08e-10],
    )


@component.add(
    name="Lahan Lainnya Hist",
    units="Ha",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def lahan_lainnya_hist():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [25221.1, 29175.7, 27795.2, 16824.3, 35835.7, 37922.5, 40700.2],
    )


@component.add(
    name="Hutan Tanaman ke Pertambangan share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def hutan_tanaman_ke_pertambangan_share():
    return np.interp(
        time_index(), [2016, 2017, 2018, 2019, 2020, 2021, 2022], [0, 0, 0, 0, 0, 0, 0]
    )


@component.add(
    name='"Hutan Tanaman ke Rawa & Badan Air share"',
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def hutan_tanaman_ke_rawa_badan_air_share():
    return np.interp(
        time_index(), [2016, 2017, 2018, 2019, 2020, 2021, 2022], [0, 0, 0, 0, 0, 0, 0]
    )


@component.add(
    name="Belukar Padang Rumput Hist",
    units="Ha",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def belukar_padang_rumput_hist():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [1156710.0, 1157980.0, 1161820.0, 1142070.0, 1134670.0, 1071260.0, 1072430.0],
    )


@component.add(
    name="Hutan Mangrove Hist",
    units="Ha",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def hutan_mangrove_hist():
    return np.interp(
        time_index(),
        [2016, 2017, 2018, 2019, 2020, 2021, 2022],
        [270117, 269443, 268656, 268076, 268068, 276289, 276259],
    )


@component.add(
    name="Lahan Lainnya ke Hutan Mangrove share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def lahan_lainnya_ke_hutan_mangrove_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [3.43e-04, 2.67e-09, 1.21e-03, 0.00e00, 1.21e-03, 0.00e00, 4.61e-04],
    )


@component.add(
    name="Belukar Padang Rumput ke Lahan Lainnya share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def belukar_padang_rumput_ke_lahan_lainnya_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [0.00407, 0.000318, 0.0012, 0.00708, 0.0034, 0.000772, 0.00281],
    )


@component.add(
    name="Hutan Tanaman to Belukar Padang Rumput share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def hutan_tanaman_to_belukar_padang_rumput_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [0.000582, 0.0039, 0.000162, 0.0, 0.00133, 0.0, 0.000995],
    )


@component.add(
    name="Belukar Padang Rumput ke Pertambangan share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def belukar_padang_rumput_ke_pertambangan_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [2.05e-04, 4.61e-05, 1.10e-03, 4.31e-04, 5.45e-04, 2.34e-04, 4.27e-04],
    )


@component.add(
    name='"Belukar Padang Rumput ke Rawa & Badan Air share"',
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def belukar_padang_rumput_ke_rawa_badan_air_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [1.93e-05, 6.60e-06, 1.37e-03, 0.00e00, 1.73e-03, 0.00e00, 5.20e-04],
    )


@component.add(
    name='"Hutan Tanaman to Hutan Primer & Sekunder share"',
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def hutan_tanaman_to_hutan_primer_sekunder_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [8.50e-05, 1.26e-09, 1.45e-05, 0.00e00, 0.00e00, 0.00e00, 1.66e-05],
    )


@component.add(
    name="Pertanian to Hutan Tanaman share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def pertanian_to_hutan_tanaman_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [1.14e-07, 0.00e00, 0.00e00, 0.00e00, 6.40e-04, 0.00e00, 1.07e-04],
    )


@component.add(
    name="Hutan Mangrove to Belukar Padang Rumput share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def hutan_mangrove_to_belukar_padang_rumput_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [0.00805, 0.000308, 0.0104, 0.0, 0.0216, 0.0, 0.00672],
    )


@component.add(
    name="Belukar Padang Rumput to Hutan Mangrove share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def belukar_padang_rumput_to_hutan_mangrove_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [3.04e-04, 7.24e-07, 1.59e-03, 0.00e00, 5.24e-03, 0.00e00, 1.19e-03],
    )


@component.add(
    name='"Belukar Padang Rumput to Hutan Primer & Sekunder share"',
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def belukar_padang_rumput_to_hutan_primer_sekunder_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [9.96e-03, 8.27e-06, 6.06e-02, 0.00e00, 6.24e-02, 0.00e00, 2.22e-02],
    )


@component.add(
    name='"Rawa & Badan Air ke Belukar Padang Rumput share"',
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def rawa_badan_air_ke_belukar_padang_rumput_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [1.03e-02, 7.22e-05, 3.71e-05, 0.00e00, 1.34e-02, 0.00e00, 3.97e-03],
    )


@component.add(
    name="Hutan Mangrove to Hutan Tanamang share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def hutan_mangrove_to_hutan_tanamang_share():
    return np.interp(
        time_index(), [2016, 2017, 2018, 2019, 2020, 2021, 2022], [0, 0, 0, 0, 0, 0, 0]
    )


@component.add(
    name='"Rawa & Badan Air ke Hutan Primer & Sekunder share"',
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def rawa_badan_air_ke_hutan_primer_sekunder_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [0.000697, 0.00176, 0.00516, 0.0, 0.00916, 0.0, 0.00279],
    )


@component.add(
    name="Hutan Mangrove to Lahan Terbangun share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def hutan_mangrove_to_lahan_terbangun_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [0.000156, 0.00127, 0.00088, 0.0, 0.000473, 0.0, 0.000464],
    )


@component.add(
    name="Belukar Padang Rumput to Lahan Terbangun share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def belukar_padang_rumput_to_lahan_terbangun_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [9.08e-04, 3.02e-04, 3.58e-03, 5.42e-05, 8.11e-04, 1.92e-05, 9.46e-04],
    )


@component.add(
    name="Hutan Tanaman to Pertanian share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def hutan_tanaman_to_pertanian_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [6.83e-05, 9.23e-11, 4.61e-03, 0.00e00, 1.04e-02, 0.00e00, 2.51e-03],
    )


@component.add(
    name='"Rawa & Badan Air ke Lahan Lainnya share"',
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def rawa_badan_air_ke_lahan_lainnya_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [0.00125, 0.0, 0.000272, 0.0, 0.000571, 0.0, 0.00035],
    )


@component.add(
    name="Hutan Mangrove to Perkebunan share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def hutan_mangrove_to_perkebunan_share():
    return np.interp(
        time_index(), [2016, 2017, 2018, 2019, 2020, 2021, 2022], [0, 0, 0, 0, 0, 0, 0]
    )


@component.add(
    name='"Perkebunan ke Rawa & Badan Air share"',
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def perkebunan_ke_rawa_badan_air_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [0.00e00, 7.46e-10, 6.26e-04, 0.00e00, 4.44e-03, 0.00e00, 8.44e-04],
    )


@component.add(
    name='"Hutan Mangrove ke Rawa & Badan Air share"',
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def hutan_mangrove_ke_rawa_badan_air_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [2.94e-04, 2.15e-05, 3.16e-03, 0.00e00, 1.83e-03, 0.00e00, 8.84e-04],
    )


@component.add(
    name='"Rawa & Badan Air ke Lahan Terbangun share"',
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def rawa_badan_air_ke_lahan_terbangun_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [0.000223, 0.000126, 0.0, 0.0, 0.00123, 0.0, 0.000263],
    )


@component.add(
    name="Hutan Mangrove to Pertanian share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def hutan_mangrove_to_pertanian_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [0.00127, 0.00182, 0.0119, 0.0, 0.0111, 0.0, 0.00435],
    )


@component.add(
    name="Pertanian ke Lahan Lainnya share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def pertanian_ke_lahan_lainnya_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [4.38e-04, 7.28e-05, 6.27e-04, 2.44e-03, 1.63e-03, 7.18e-04, 9.88e-04],
    )


@component.add(
    name="Perkebunan to Belukar Padang Rumput share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def perkebunan_to_belukar_padang_rumput_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [0.00874, 0.000345, 0.0534, 0.0, 0.00283, 0.0, 0.0109],
    )


@component.add(
    name='"Rawa & Badan Air ke Perkebunan share"',
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def rawa_badan_air_ke_perkebunan_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [0.00e00, 5.98e-09, 3.80e-09, 0.00e00, 0.00e00, 0.00e00, 1.63e-09],
    )


@component.add(
    name='"Pertanian ke Rawa & Badan Air share"',
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def pertanian_ke_rawa_badan_air_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [5.90e-05, 1.10e-07, 1.01e-03, 0.00e00, 1.25e-03, 0.00e00, 3.86e-04],
    )


@component.add(
    name='"Rawa & Badan Air ke Pertambangan share"',
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def rawa_badan_air_ke_pertambangan_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [0.00e00, 1.32e-10, 0.00e00, 0.00e00, 1.29e-03, 0.00e00, 2.16e-04],
    )


@component.add(
    name="Perkebunan Hist",
    units="Ha",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def perkebunan_hist():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [34173.2, 36381.1, 37101.4, 44695.9, 44695.9, 44652.5, 44652.5],
    )


@component.add(
    name="Pertambangan ke Hutan Mangrove share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def pertambangan_ke_hutan_mangrove_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [0.000701, 0.0, 0.0, 0.0, 0.000385, 0.0, 0.000181],
    )


@component.add(
    name='"Rawa & Badan Air ke Pertanian share"',
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def rawa_badan_air_ke_pertanian_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [0.00624, 0.000417, 0.00105, 0.0, 0.00328, 0.0, 0.00183],
    )


@component.add(
    name="Perkebunan ke Lahan Lainnya share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def perkebunan_ke_lahan_lainnya_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [1.06e-05, 2.05e-04, 1.21e-04, 0.00e00, 0.00e00, 0.00e00, 5.61e-05],
    )


@component.add(
    name="Pertanian to Hutan Mangrove share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def pertanian_to_hutan_mangrove_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [6.22e-04, 1.96e-08, 2.31e-03, 0.00e00, 5.20e-03, 0.00e00, 1.36e-03],
    )


@component.add(
    name="Perkebunan ke Pertambangan share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def perkebunan_ke_pertambangan_share():
    return np.interp(
        time_index(), [2016, 2017, 2018, 2019, 2020, 2021, 2022], [0, 0, 0, 0, 0, 0, 0]
    )


@component.add(
    name='"Hutan Primer & Sekunder to Pertanian share"',
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def hutan_primer_sekunder_to_pertanian_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [4.84e-03, 1.97e-03, 5.33e-03, 2.34e-04, 7.51e-03, 5.82e-05, 3.32e-03],
    )


@component.add(
    name="Hutan Mangrove ke Pertambangan share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def hutan_mangrove_ke_pertambangan_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [0.00e00, 0.00e00, 2.24e-05, 0.00e00, 4.80e-05, 0.00e00, 1.17e-05],
    )


@component.add(
    name='"Hutan Primer & Sekunder Hist"',
    units="Ha",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def hutan_primer_sekunder_hist():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [4723870.0, 4772940.0, 4758360.0, 4837920.0, 4826960.0, 4866680.0, 4862550.0],
    )


@component.add(
    name="Lahan Lainnya ke Lahan Terbangun share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def lahan_lainnya_ke_lahan_terbangun_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [0.000246, 0.0, 0.00161, 0.000943, 0.00129, 0.0, 0.000681],
    )


@component.add(
    name="Hutan Tanaman to Lahan Terbangun share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def hutan_tanaman_to_lahan_terbangun_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [0.00e00, 0.00e00, 0.00e00, 0.00e00, 9.53e-05, 0.00e00, 1.59e-05],
    )


@component.add(
    name="Perkebunan to Hutan Mangrove share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def perkebunan_to_hutan_mangrove_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [0.0032, 0.0, 0.00167, 0.0, 0.00743, 0.0, 0.00205],
    )


@component.add(
    name='"Perkebunan to Hutan Primer & Sekunder share"',
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def perkebunan_to_hutan_primer_sekunder_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [0.00974, 0.0, 0.0122, 0.0, 0.0039, 0.0, 0.0043],
    )


@component.add(
    name='"Rawa & Badan Air ke Hutan Mangrove share"',
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def rawa_badan_air_ke_hutan_mangrove_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [0.00545, 0.00822, 0.00691, 0.0, 0.0263, 0.0, 0.00781],
    )


@component.add(
    name="Lahan Lainnya ke Pertambangan share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def lahan_lainnya_ke_pertambangan_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [3.03e-04, 8.75e-10, 3.32e-02, 3.87e-03, 1.38e-02, 3.42e-03, 9.10e-03],
    )


@component.add(
    name="Perkebunan to Hutan Tanamang share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def perkebunan_to_hutan_tanamang_share():
    return np.interp(
        time_index(), [2016, 2017, 2018, 2019, 2020, 2021, 2022], [0, 0, 0, 0, 0, 0, 0]
    )


@component.add(
    name='"Pertambangan ke Rawa & Badan Air share"',
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def pertambangan_ke_rawa_badan_air_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [4.90e-10, 0.00e00, 0.00e00, 0.00e00, 0.00e00, 0.00e00, 8.17e-11],
    )


@component.add(
    name="Lahan Lainnya ke Pertanian share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def lahan_lainnya_ke_pertanian_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [0.159, 0.000666, 0.0427, 0.00535, 0.106, 0.0, 0.0523],
    )


@component.add(
    name="Perkebunan to Lahan Terbangun share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def perkebunan_to_lahan_terbangun_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [6.13e-03, 4.60e-03, 4.04e-03, 0.00e00, 7.71e-05, 0.00e00, 2.48e-03],
    )


@component.add(
    name="Pertambangan ke Hutan Tanaman share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def pertambangan_ke_hutan_tanaman_share():
    return np.interp(
        time_index(), [2016, 2017, 2018, 2019, 2020, 2021, 2022], [0, 0, 0, 0, 0, 0, 0]
    )


@component.add(
    name='"Pertanian to Hutan Primer & Sekunder share"',
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def pertanian_to_hutan_primer_sekunder_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [6.37e-02, 4.35e-05, 3.59e-02, 0.00e00, 2.87e-02, 0.00e00, 2.14e-02],
    )


@component.add(
    name="Hutan Tanaman to Hutan Mangrove share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def hutan_tanaman_to_hutan_mangrove_share():
    return np.interp(
        time_index(), [2016, 2017, 2018, 2019, 2020, 2021, 2022], [0, 0, 0, 0, 0, 0, 0]
    )


@component.add(
    name="Perkebunan to Pertanian share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def perkebunan_to_pertanian_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [2.16e-02, 6.26e-03, 2.80e-02, 0.00e00, 2.75e-05, 0.00e00, 9.32e-03],
    )


@component.add(
    name="Lahan Terbangun to Belukar Padang Rumput share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def lahan_terbangun_to_belukar_padang_rumput_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [0.0102, 0.0039, 0.0239, 0.0, 0.00915, 0.0, 0.00785],
    )


@component.add(
    name='"Pertambangan ke Hutan Primer & Sekunder share"',
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def pertambangan_ke_hutan_primer_sekunder_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [4.76e-02, 1.79e-08, 2.07e-03, 0.00e00, 8.72e-03, 0.00e00, 9.73e-03],
    )


@component.add(
    name='"Hutan Mangrove to Hutan Primer & Sekunder share"',
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def hutan_mangrove_to_hutan_primer_sekunder_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [2.15e-04, 2.41e-05, 7.17e-03, 0.00e00, 2.67e-02, 0.00e00, 5.69e-03],
    )


@component.add(
    name="Pertanian ke Pertambangan share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def pertanian_ke_pertambangan_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [1.14e-06, 7.29e-05, 1.40e-04, 2.95e-04, 2.21e-04, 4.88e-05, 1.30e-04],
    )


@component.add(
    name="Pertanian to Lahan Terbangun share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def pertanian_to_lahan_terbangun_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [2.79e-03, 1.17e-03, 4.70e-03, 5.45e-05, 6.95e-03, 6.22e-05, 2.62e-03],
    )


@component.add(
    name="Pertambangan ke Belukar Padang Rumput share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def pertambangan_ke_belukar_padang_rumput_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [0.000897, 0.0931, 0.00349, 0.0, 0.00967, 0.0, 0.0179],
    )


@component.add(
    name="Lahan Terbangun ke Lahan Lainnya share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def lahan_terbangun_ke_lahan_lainnya_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [3.84e-05, 3.49e-04, 5.32e-03, 0.00e00, 1.46e-03, 0.00e00, 1.19e-03],
    )


@component.add(
    name="Lahan Lainnya ke Belukar Padang Rumput share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def lahan_lainnya_ke_belukar_padang_rumput_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [0.018, 0.064, 0.307, 0.103, 0.115, 0.0184, 0.104],
    )


@component.add(
    name="Lahan Terbangun ke Pertambangan share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def lahan_terbangun_ke_pertambangan_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [0.00e00, 0.00e00, 5.94e-04, 0.00e00, 0.00e00, 0.00e00, 9.90e-05],
    )


@component.add(
    name='"Hutan Primer & Sekunder to Hutan Mangrove share"',
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def hutan_primer_sekunder_to_hutan_mangrove_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [6.72e-05, 4.08e-06, 6.14e-04, 0.00e00, 2.49e-03, 0.00e00, 5.29e-04],
    )


@component.add(
    name='"Lahan Lainnya ke Hutan Primer & Sekunder share"',
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def lahan_lainnya_ke_hutan_primer_sekunder_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [2.40e-02, 9.14e-05, 1.56e-02, 0.00e00, 2.79e-02, 0.00e00, 1.13e-02],
    )


@component.add(
    name="Hutan Mangrove ke Lahan Lainnya share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def hutan_mangrove_ke_lahan_lainnya_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [3.11e-04, 3.02e-06, 1.68e-04, 2.93e-05, 5.69e-03, 1.06e-04, 1.05e-03],
    )


@component.add(
    name='"Lahan Lainnya ke Rawa & Badan Air share"',
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def lahan_lainnya_ke_rawa_badan_air_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [0.00e00, 6.88e-12, 1.47e-02, 0.00e00, 2.42e-02, 0.00e00, 6.48e-03],
    )


@component.add(
    name="Lahan Lainnya ke Perkebunan share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def lahan_lainnya_ke_perkebunan_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [2.17e-06, 0.00e00, 1.20e-01, 0.00e00, 1.26e-04, 0.00e00, 2.00e-02],
    )


@component.add(
    name="Pertambangan ke Perkebunan share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def pertambangan_ke_perkebunan_share():
    return np.interp(
        time_index(), [2016, 2017, 2018, 2019, 2020, 2021, 2022], [0, 0, 0, 0, 0, 0, 0]
    )


@component.add(
    name="Pertambangan ke Lahan Lainnya share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def pertambangan_ke_lahan_lainnya_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [0.0, 0.0, 0.00575, 0.0, 0.0348, 0.0, 0.00676],
    )


@component.add(
    name="Lahan Terbangun Hist",
    units="Ha",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def lahan_terbangun_hist():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [62476.2, 62068.1, 57032.9, 65062.8, 65189.5, 70726.3, 70846.5],
    )


@component.add(
    name='"Rawa & Badan Air HIst"',
    units="Ha",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def rawa_badan_air_hist():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [15209.2, 15038.6, 14893.6, 19457.2, 19457.2, 24984.5, 24984.5],
    )


@component.add(
    name='"Rawa & Badan Air ke Hutan Tanaman share"',
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def rawa_badan_air_ke_hutan_tanaman_share():
    return np.interp(
        time_index(), [2016, 2017, 2018, 2019, 2020, 2021, 2022], [0, 0, 0, 0, 0, 0, 0]
    )


@component.add(
    name="Hutan Tanaman to Perkebunan share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def hutan_tanaman_to_perkebunan_share():
    return np.interp(
        time_index(), [2016, 2017, 2018, 2019, 2020, 2021, 2022], [0, 0, 0, 0, 0, 0, 0]
    )


@component.add(
    name="Pertambangan ke Lahan Terbangun share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def pertambangan_ke_lahan_terbangun_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [0.0, 0.0, 0.00299, 0.0, 0.0, 0.0, 0.000498],
    )


@component.add(
    name="Pertambangan ke Pertanian share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def pertambangan_ke_pertanian_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [0.00113, 0.0, 0.0278, 0.0, 0.000827, 0.0, 0.00496],
    )


@component.add(
    name='"Hutan Primer & Sekunder ke Rawa & Badan Air share"',
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def hutan_primer_sekunder_ke_rawa_badan_air_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [8.79e-07, 1.40e-07, 8.23e-05, 0.00e00, 2.66e-04, 0.00e00, 5.83e-05],
    )


@component.add(
    name="Lahan Lainnya ke Hutan Tanamang share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def lahan_lainnya_ke_hutan_tanamang_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [0.00e00, 1.08e-09, 2.62e-09, 0.00e00, 4.33e-03, 0.00e00, 7.22e-04],
    )


@component.add(
    name="Pertanian to Belukar Padang Rumput share",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def pertanian_to_belukar_padang_rumput_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [4.91e-03, 6.40e-03, 4.87e-02, 3.79e-04, 1.65e-02, 9.26e-05, 1.28e-02],
    )


@component.add(
    name='"Lahan Terbangun ke Rawa & Badan Air share"',
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def lahan_terbangun_ke_rawa_badan_air_share():
    return np.interp(
        time_index(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [2.66e-05, 1.76e-09, 8.86e-05, 0.00e00, 4.80e-04, 0.00e00, 9.93e-05],
    )


@component.add(
    name="Ambang Batas Penduduk Air",
    units="jiwa",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_ketersediaan_air_bisa_digunakan": 1,
        "kebutuhan_air_per_kapita": 1,
    },
)
def ambang_batas_penduduk_air():
    return total_ketersediaan_air_bisa_digunakan() / kebutuhan_air_per_kapita()


@component.add(
    name="Kebutuhan Lahan Terbangun",
    units="Ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"lahan_terbangun_per_kapita": 1, "populasi_historisprojeksi": 1},
)
def kebutuhan_lahan_terbangun():
    return lahan_terbangun_per_kapita() * populasi_historisprojeksi()


@component.add(
    name="Ambang Batas Penduduk Pangan",
    units="jiwa",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"biokapasitas_pangan": 1, "lahan_pangan_per_kapita": 1},
)
def ambang_batas_penduduk_pangan():
    return biokapasitas_pangan() / lahan_pangan_per_kapita()


@component.add(
    name="Laju Perubahan Lahan Terbangun per Kapita",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def laju_perubahan_lahan_terbangun_per_kapita():
    """
    ([(2016,0)-(2025,0.3)],(2016,0.205325),(2017,0.164053),(2018,0.136615),(201 9,0.115691),(2020,0.122478),(2021,0.091922 ),(2022,0.113174),(2025,0.03) )
    """
    return np.interp(
        time(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0, 2023.0],
        [-0.16, 0.16, -0.21, 0.27, -0.19, 0.06, 0.04, 0.01],
    )


@component.add(
    name="Populasi Papua Hist",
    units="jiwa",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def populasi_papua_hist():
    return np.interp(
        time(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0],
        [4499530.0, 4670860.0, 4848740.0, 5033460.0, 5241530.0],
    )


@component.add(
    name="Lahan jasling kehati tinggi dan sangat tinggi",
    units="Ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "belukar_rumput_jasling_kehati_tinggi_dan_sangat_tinggi": 1,
        "hutan_primer_sekunder_jasling_kehati_tinggi_dan_sangat_tinggi": 1,
        "hutan_tanaman_jasling_kehati_tinggi_dan_sangat_tinggi": 1,
        "perkebunan_jasling_kehati_tinggi_dan_sangat_tinggi": 1,
    },
)
def lahan_jasling_kehati_tinggi_dan_sangat_tinggi():
    return (
        belukar_rumput_jasling_kehati_tinggi_dan_sangat_tinggi()
        + hutan_primer_sekunder_jasling_kehati_tinggi_dan_sangat_tinggi()
        + hutan_tanaman_jasling_kehati_tinggi_dan_sangat_tinggi()
        + perkebunan_jasling_kehati_tinggi_dan_sangat_tinggi()
    )


@component.add(
    name='"Hutan Primer & Sekunder jasling kehati tinggi dan sangat tinggi"',
    units="Ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hutan_primer_sekunder": 1,
        "fraksi_jasling_kehati_tinggi_dan_sangat_tinggi_hutan_primer_dan_sekunder": 1,
    },
)
def hutan_primer_sekunder_jasling_kehati_tinggi_dan_sangat_tinggi():
    return (
        hutan_primer_sekunder()
        * fraksi_jasling_kehati_tinggi_dan_sangat_tinggi_hutan_primer_dan_sekunder()
    )


@component.add(
    name="fraksi jasling kehati tinggi dan sangat tinggi perkebunan",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def fraksi_jasling_kehati_tinggi_dan_sangat_tinggi_perkebunan():
    return 0.22


@component.add(
    name="fraksi jasling kehati tinggi dan sangat tinggi belukar padang rumput",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def fraksi_jasling_kehati_tinggi_dan_sangat_tinggi_belukar_padang_rumput():
    return 0.99


@component.add(
    name="fraksi jasling kehati tinggi dan sangat tinggi hutan primer dan sekunder",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def fraksi_jasling_kehati_tinggi_dan_sangat_tinggi_hutan_primer_dan_sekunder():
    return 0.82


@component.add(
    name="Perkebunan jasling kehati tinggi dan sangat tinggi",
    units="Ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fraksi_jasling_kehati_tinggi_dan_sangat_tinggi_perkebunan": 1,
        "perkebunan": 1,
    },
)
def perkebunan_jasling_kehati_tinggi_dan_sangat_tinggi():
    return fraksi_jasling_kehati_tinggi_dan_sangat_tinggi_perkebunan() * perkebunan()


@component.add(
    name="Hutan tanaman jasling kehati tinggi dan sangat tinggi",
    units="Ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fraksi_jasling_kehati_tinggi_dan_sangat_tinggi_hutan_tanaman": 1,
        "hutan_tanaman": 1,
    },
)
def hutan_tanaman_jasling_kehati_tinggi_dan_sangat_tinggi():
    return (
        fraksi_jasling_kehati_tinggi_dan_sangat_tinggi_hutan_tanaman() * hutan_tanaman()
    )


@component.add(
    name="fraksi jasling kehati tinggi dan sangat tinggi hutan tanaman",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def fraksi_jasling_kehati_tinggi_dan_sangat_tinggi_hutan_tanaman():
    return 0.38


@component.add(
    name="Rasio jasa lingkungan kehati tinggi dan sangat tinggi",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"lahan_jasling_kehati_tinggi_dan_sangat_tinggi": 1, "total_lahan": 1},
)
def rasio_jasa_lingkungan_kehati_tinggi_dan_sangat_tinggi():
    return lahan_jasling_kehati_tinggi_dan_sangat_tinggi() / total_lahan()


@component.add(
    name="Belukar rumput jasling kehati tinggi dan sangat tinggi",
    units="Ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "belukar_padang_rumput": 1,
        "fraksi_jasling_kehati_tinggi_dan_sangat_tinggi_belukar_padang_rumput": 1,
    },
)
def belukar_rumput_jasling_kehati_tinggi_dan_sangat_tinggi():
    return (
        belukar_padang_rumput()
        * fraksi_jasling_kehati_tinggi_dan_sangat_tinggi_belukar_padang_rumput()
    )


@component.add(name="mult", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def mult():
    return 1.45


@component.add(
    name="KLR Proxy",
    units="JutaRp/jiwa",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_klr_proxy": 1},
    other_deps={
        "_integ_klr_proxy": {
            "initial": {"kapital_awal": 1, "tenaga_kerja_awal": 1},
            "step": {"perubahan_klr_proxy": 1},
        }
    },
)
def klr_proxy():
    return _integ_klr_proxy()


_integ_klr_proxy = Integ(
    lambda: perubahan_klr_proxy(),
    lambda: kapital_awal() / tenaga_kerja_awal(),
    "_integ_klr_proxy",
)


@component.add(
    name="laju perubahan KLR",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def laju_perubahan_klr():
    return np.interp(
        time(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0, 2023.0, 2030.0],
        [
            0.0572929,
            0.0572929,
            0.0572929,
            0.0572929,
            0.0572929,
            0.0572929,
            0.0572929,
            0.0572929,
            0.037,
        ],
    )


@component.add(
    name="Tenaga Kerja",
    units="jiwa",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"angkatan_kerja": 1, "tenaga_kerja_dari_klr": 1},
)
def tenaga_kerja():
    return np.minimum(angkatan_kerja() * 0.975, tenaga_kerja_dari_klr())


@component.add(
    name="Tk Pengangguran",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pengangguran": 1, "angkatan_kerja": 1},
)
def tk_pengangguran():
    return pengangguran() / angkatan_kerja()


@component.add(
    name="Tenaga kerja dari KLR",
    units="jiwa",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"kapital": 1, "klr_proxy": 1},
)
def tenaga_kerja_dari_klr():
    return kapital() / klr_proxy()


@component.add(
    name="Perubahan KLR Proxy",
    units="JutaRp/(tahun*jiwa)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"klr_proxy": 1, "laju_perubahan_klr": 1},
)
def perubahan_klr_proxy():
    return klr_proxy() * laju_perubahan_klr()


@component.add(
    name="Nilai Tambah Pertanian Hist",
    units="JutaRp/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def nilai_tambah_pertanian_hist():
    return np.interp(
        time(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0, 2023.0],
        [
            24262500.0,
            24985900.0,
            25265200.0,
            25386500.0,
            24600800.0,
            24443100.0,
            24266700.0,
            24390000.0,
        ],
    )


@component.add(
    name="Nilai Tambah Pertanian Init",
    units="JutaRp/tahun",
    comp_type="Stateful",
    comp_subtype="Initial",
    depends_on={"_initial_nilai_tambah_pertanian_init": 1},
    other_deps={
        "_initial_nilai_tambah_pertanian_init": {
            "initial": {"nilai_tambah_pertanian_hist": 1},
            "step": {},
        }
    },
)
def nilai_tambah_pertanian_init():
    return _initial_nilai_tambah_pertanian_init()


_initial_nilai_tambah_pertanian_init = Initial(
    lambda: nilai_tambah_pertanian_hist(), "_initial_nilai_tambah_pertanian_init"
)


@component.add(
    name="Tes", units="Ha/tahun", comp_type="Constant", comp_subtype="Normal"
)
def tes():
    return 1


@component.add(
    name="Produktivitas Pertanian",
    units="JutaRp/tahun/Ha",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def produktivitas_pertanian():
    return np.interp(
        time(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0, 2023.0],
        [9.65, 10.15, 10.48, 10.75, 10.57, 10.66, 10.75, 7.77],
    )


@component.add(
    name="Total Peralihan ke Perkebunan",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "belukar_padang_rumput_to_perkebunan_hist": 1,
        "hutan_mangrove_to_perkebunan_hist": 1,
        "hutan_primer_hutan_sekunder_to_perkebunan_hist": 1,
        "hutan_tanaman_to_perkebunan_hist": 1,
        "lahan_lainnya_ke_perkebunan_hist": 1,
        "lahan_terbangun_to_perkebunan_hist": 1,
        "pertanian_to_perkebunan_hist": 1,
        "pertambangan_ke_perkebunan_hist": 1,
        "rawa_badan_air_ke_perkebunan_hist": 1,
        "tes": 1,
    },
)
def total_peralihan_ke_perkebunan():
    return (
        belukar_padang_rumput_to_perkebunan_hist()
        + hutan_mangrove_to_perkebunan_hist()
        + hutan_primer_hutan_sekunder_to_perkebunan_hist()
        + hutan_tanaman_to_perkebunan_hist()
        + lahan_lainnya_ke_perkebunan_hist()
        + lahan_terbangun_to_perkebunan_hist()
        + pertanian_to_perkebunan_hist()
        + pertambangan_ke_perkebunan_hist()
        + rawa_badan_air_ke_perkebunan_hist()
        + tes()
    )


@component.add(
    name="Nilai Tambah Perkebunan Hist",
    units="JutaRp/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def nilai_tambah_perkebunan_hist():
    return np.interp(
        time(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0, 2023.0],
        [
            4974460.0,
            5144800.0,
            5236510.0,
            5422250.0,
            5479780.0,
            5533190.0,
            5597100.0,
            5624000.0,
        ],
    )


@component.add(
    name="Nilai Tambah Perkebunan Init",
    units="JutaRp/tahun",
    comp_type="Stateful",
    comp_subtype="Initial",
    depends_on={"_initial_nilai_tambah_perkebunan_init": 1},
    other_deps={
        "_initial_nilai_tambah_perkebunan_init": {
            "initial": {"nilai_tambah_perkebunan_hist": 1},
            "step": {},
        }
    },
)
def nilai_tambah_perkebunan_init():
    return _initial_nilai_tambah_perkebunan_init()


_initial_nilai_tambah_perkebunan_init = Initial(
    lambda: nilai_tambah_perkebunan_hist(), "_initial_nilai_tambah_perkebunan_init"
)


@component.add(
    name="Pertanian to Lahan Terbangun Indicated",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "peralihan_lahan_terbangun_ydi": 1,
        "share_pertanian_to_lahan_terbangun": 1,
    },
)
def pertanian_to_lahan_terbangun_indicated():
    return peralihan_lahan_terbangun_ydi() * share_pertanian_to_lahan_terbangun()


@component.add(
    name="Kebutuhan Lahan Pertanian",
    units="Ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"nilai_tambah_pertanian": 1, "produktivitas_pertanian": 1},
)
def kebutuhan_lahan_pertanian():
    return nilai_tambah_pertanian() / produktivitas_pertanian()


@component.add(
    name="Pertanian to Perkebunan Hist",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def pertanian_to_perkebunan_hist():
    return np.interp(time(), [2016, 2017, 2018, 2019], [1562, 1645, 774, 1291])


@component.add(
    name="Lahan Terbangun to Perkebunan Hist",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def lahan_terbangun_to_perkebunan_hist():
    return np.interp(time(), [2016, 2017, 2018, 2019], [123, 1091, 0, 1662])


@component.add(
    name="Lahan Terbangun to Perkebunan Indicated",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "peralihan_lahan_perkebunan_ydi": 1,
        "share_lahan_terbangun_to_perkebunan": 1,
    },
)
def lahan_terbangun_to_perkebunan_indicated():
    return peralihan_lahan_perkebunan_ydi() * share_lahan_terbangun_to_perkebunan()


@component.add(
    name="Share Hutan Tanaman to Perkebunan",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hutan_tanaman_to_perkebunan_hist": 1,
        "total_peralihan_ke_perkebunan": 1,
    },
)
def share_hutan_tanaman_to_perkebunan():
    return hutan_tanaman_to_perkebunan_hist() / total_peralihan_ke_perkebunan()


@component.add(
    name="Share Hutan Tanaman to Pertanian",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hutan_tanaman_to_pertanian_hist": 1,
        "total_peralihan_ke_pertanian": 1,
    },
)
def share_hutan_tanaman_to_pertanian():
    return hutan_tanaman_to_pertanian_hist() / total_peralihan_ke_pertanian()


@component.add(
    name="Lahan Terbangun to Pertanian Hist",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def lahan_terbangun_to_pertanian_hist():
    return np.interp(time(), [2016, 2017, 2018, 2019], [601, 24071, 67, 16385])


@component.add(
    name="Lahan Terbangun to Pertanian Indicated",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "peralihan_lahan_pertanian_ydi": 1,
        "share_lahan_terbangun_to_pertanian": 1,
    },
)
def lahan_terbangun_to_pertanian_indicated():
    return peralihan_lahan_pertanian_ydi() * share_lahan_terbangun_to_pertanian()


@component.add(
    name="Perubahan Nilai Tambah Pertanian",
    units="JutaRp/(tahun*tahun)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fraksi_perubahan_nilai_tambah_pertanian": 1,
        "nilai_tambah_pertanian": 1,
    },
)
def perubahan_nilai_tambah_pertanian():
    return fraksi_perubahan_nilai_tambah_pertanian() * nilai_tambah_pertanian()


@component.add(
    name="Fraksi Perubahan Nilai Tambah Perkebunan",
    units="1/tahun",
    comp_type="Constant",
    comp_subtype="Normal",
)
def fraksi_perubahan_nilai_tambah_perkebunan():
    return 0.025


@component.add(
    name="Fraksi Perubahan Nilai Tambah Pertanian",
    units="1/tahun",
    comp_type="Constant",
    comp_subtype="Normal",
)
def fraksi_perubahan_nilai_tambah_pertanian():
    return 0.01


@component.add(
    name="Share Perkebunan to Lahan Terbangun",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "perkebunan_to_lahan_terbangun_hist": 1,
        "total_peralihan_ke_lahan_terbangun": 1,
    },
)
def share_perkebunan_to_lahan_terbangun():
    return perkebunan_to_lahan_terbangun_hist() / total_peralihan_ke_lahan_terbangun()


@component.add(
    name="Gap Lahan Perkebunan",
    units="Ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"kebutuhan_lahan_perkebunan": 1, "perkebunan": 1},
)
def gap_lahan_perkebunan():
    return np.maximum(0, kebutuhan_lahan_perkebunan() - perkebunan())


@component.add(
    name="Gap Lahan Pertanian",
    units="Ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"kebutuhan_lahan_pertanian": 1, "pertanian": 1},
)
def gap_lahan_pertanian():
    return np.maximum(0, kebutuhan_lahan_pertanian() - pertanian())


@component.add(
    name="Gap Lahan Terbangun",
    units="Ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"kebutuhan_lahan_terbangun": 1, "lahan_terbangun": 1},
)
def gap_lahan_terbangun():
    return np.maximum(0, kebutuhan_lahan_terbangun() - lahan_terbangun())


@component.add(
    name="Share Pertambangan ke Pertanian",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pertambangan_ke_pertanian_hist": 1, "total_peralihan_ke_pertanian": 1},
)
def share_pertambangan_ke_pertanian():
    return pertambangan_ke_pertanian_hist() / total_peralihan_ke_pertanian()


@component.add(
    name="Produktivitas Perkebunan",
    units="JutaRp/tahun/Ha",
    comp_type="Constant",
    comp_subtype="Normal",
)
def produktivitas_perkebunan():
    return 1000


@component.add(
    name='"Share Rawa & Badan Air ke Lahan Terbangun"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "rawa_badan_air_ke_lahan_terbangun_hist": 1,
        "total_peralihan_ke_lahan_terbangun": 1,
    },
)
def share_rawa_badan_air_ke_lahan_terbangun():
    return (
        rawa_badan_air_ke_lahan_terbangun_hist() / total_peralihan_ke_lahan_terbangun()
    )


@component.add(
    name='"Share Rawa & Badan Air ke Perkebunan"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "rawa_badan_air_ke_perkebunan_hist": 1,
        "total_peralihan_ke_perkebunan": 1,
    },
)
def share_rawa_badan_air_ke_perkebunan():
    return rawa_badan_air_ke_perkebunan_hist() / total_peralihan_ke_perkebunan()


@component.add(
    name='"Share Rawa & Badan Air ke Pertanian"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "rawa_badan_air_ke_pertanian_hist": 1,
        "total_peralihan_ke_pertanian": 1,
    },
)
def share_rawa_badan_air_ke_pertanian():
    return rawa_badan_air_ke_pertanian_hist() / total_peralihan_ke_pertanian()


@component.add(
    name='"Hutan Primer & Hutan Sekunder to Lahan Terbangun Hist"',
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def hutan_primer_hutan_sekunder_to_lahan_terbangun_hist():
    return np.interp(
        time(),
        [2016, 2017, 2018, 2019, 2020, 2021, 2022],
        [683, 29, 381, 0, 368, 12, 245],
    )


@component.add(
    name='"Hutan Primer & Hutan Sekunder to Lahan Terbangun Indicated"',
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "peralihan_lahan_terbangun_ydi": 1,
        "share_hutan_primer_hutan_sekunder_to_lahan_terbangun": 1,
    },
)
def hutan_primer_hutan_sekunder_to_lahan_terbangun_indicated():
    return (
        peralihan_lahan_terbangun_ydi()
        * share_hutan_primer_hutan_sekunder_to_lahan_terbangun()
    )


@component.add(
    name="Perkebunan to Pertanian Hist",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def perkebunan_to_pertanian_hist():
    return np.interp(time(), [2016, 2017, 2018, 2019], [52, 3723, 139, 1521])


@component.add(
    name="Pertambangan ke Lahan Terbangun Hist",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def pertambangan_ke_lahan_terbangun_hist():
    return np.interp(
        time(), [2016, 2017, 2018, 2019, 2020, 2021, 2022], [0, 0, 13, 0, 0, 0, 2]
    )


@component.add(
    name="Pertambangan ke Lahan Terbangun Indicated",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "peralihan_lahan_terbangun_ydi": 1,
        "share_pertambangan_ke_lahan_terbangun": 1,
    },
)
def pertambangan_ke_lahan_terbangun_indicated():
    return peralihan_lahan_terbangun_ydi() * share_pertambangan_ke_lahan_terbangun()


@component.add(
    name="Hutan Tanaman to Lahan Terbangun Hist",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def hutan_tanaman_to_lahan_terbangun_hist():
    return np.interp(
        time(), [2016, 2017, 2018, 2019, 2020, 2021, 2022], [0, 0, 0, 0, 3, 0, 1]
    )


@component.add(
    name="Nilai Tambah Perkebunan",
    units="JutaRp/tahun",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_nilai_tambah_perkebunan": 1},
    other_deps={
        "_integ_nilai_tambah_perkebunan": {
            "initial": {"nilai_tambah_perkebunan_init": 1},
            "step": {"perubahan_nilai_tambah_perkebunan": 1},
        }
    },
)
def nilai_tambah_perkebunan():
    return _integ_nilai_tambah_perkebunan()


_integ_nilai_tambah_perkebunan = Integ(
    lambda: perubahan_nilai_tambah_perkebunan(),
    lambda: nilai_tambah_perkebunan_init(),
    "_integ_nilai_tambah_perkebunan",
)


@component.add(
    name="Nilai Tambah Pertanian",
    units="JutaRp/tahun",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_nilai_tambah_pertanian": 1},
    other_deps={
        "_integ_nilai_tambah_pertanian": {
            "initial": {"nilai_tambah_pertanian_init": 1},
            "step": {"perubahan_nilai_tambah_pertanian": 1},
        }
    },
)
def nilai_tambah_pertanian():
    return _integ_nilai_tambah_pertanian()


_integ_nilai_tambah_pertanian = Integ(
    lambda: perubahan_nilai_tambah_pertanian(),
    lambda: nilai_tambah_pertanian_init(),
    "_integ_nilai_tambah_pertanian",
)


@component.add(
    name="Hutan Tanaman to Perkebunan Indicated",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "peralihan_lahan_perkebunan_ydi": 1,
        "share_hutan_tanaman_to_perkebunan": 1,
    },
)
def hutan_tanaman_to_perkebunan_indicated():
    return peralihan_lahan_perkebunan_ydi() * share_hutan_tanaman_to_perkebunan()


@component.add(
    name="Belukar Padang Rumput to Lahan Terbangun Hist",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def belukar_padang_rumput_to_lahan_terbangun_hist():
    return np.interp(
        time(),
        [2016, 2017, 2018, 2019, 2020, 2021, 2022],
        [1050, 350, 4162, 62, 920, 21, 1094],
    )


@component.add(
    name="Belukar Padang Rumput to Lahan Terbangun Indicated",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "peralihan_lahan_terbangun_ydi": 1,
        "share_belukar_padang_rumput_to_lahan_terbangun": 1,
    },
)
def belukar_padang_rumput_to_lahan_terbangun_indicated():
    return (
        peralihan_lahan_terbangun_ydi()
        * share_belukar_padang_rumput_to_lahan_terbangun()
    )


@component.add(
    name="Hutan Tanaman to Pertanian Hist",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def hutan_tanaman_to_pertanian_hist():
    return np.interp(time(), [2016, 2017, 2018, 2019], [0, 0, 0, 0])


@component.add(
    name="Hutan Tanaman to Pertanian Indicated",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "peralihan_lahan_pertanian_ydi": 1,
        "share_hutan_tanaman_to_pertanian": 1,
    },
)
def hutan_tanaman_to_pertanian_indicated():
    return peralihan_lahan_pertanian_ydi() * share_hutan_tanaman_to_pertanian()


@component.add(
    name="Belukar Padang Rumput to Perkebunan Hist",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def belukar_padang_rumput_to_perkebunan_hist():
    return np.interp(time(), [2016, 2017, 2018, 2019], [5879, 25063, 724, 3747])


@component.add(
    name="Belukar Padang Rumput to Perkebunan Indicated",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "peralihan_lahan_perkebunan_ydi": 1,
        "share_belukar_padang_rumput_to_perkebunan": 1,
    },
)
def belukar_padang_rumput_to_perkebunan_indicated():
    return (
        peralihan_lahan_perkebunan_ydi() * share_belukar_padang_rumput_to_perkebunan()
    )


@component.add(
    name="Hutan Mangrove to Lahan Terbangun Hist",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def hutan_mangrove_to_lahan_terbangun_hist():
    return np.interp(
        time(),
        [2016, 2017, 2018, 2019, 2020, 2021, 2022],
        [42, 344, 236, 0, 127, 0, 125],
    )


@component.add(
    name="Perkebunan to Pertanian Indicated",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"peralihan_lahan_pertanian_ydi": 1, "share_perkebunan_to_pertanian": 1},
)
def perkebunan_to_pertanian_indicated():
    return peralihan_lahan_pertanian_ydi() * share_perkebunan_to_pertanian()


@component.add(
    name="Belukar Padang Rumput to Pertanian Hist",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def belukar_padang_rumput_to_pertanian_hist():
    return np.interp(time(), [2016, 2017, 2018, 2019], [6004, 54110, 4283, 54391])


@component.add(
    name="Belukar Padang Rumput to Pertanian Indicated",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "peralihan_lahan_pertanian_ydi": 1,
        "share_belukar_padang_rumput_to_pertanian": 1,
    },
)
def belukar_padang_rumput_to_pertanian_indicated():
    return peralihan_lahan_pertanian_ydi() * share_belukar_padang_rumput_to_pertanian()


@component.add(
    name="Peralihan Lahan Perkebunan Ydi",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"gap_lahan_perkebunan": 1, "waktu_peralihan_lahan_perkebunan": 1},
)
def peralihan_lahan_perkebunan_ydi():
    return gap_lahan_perkebunan() / waktu_peralihan_lahan_perkebunan()


@component.add(
    name="Peralihan Lahan Pertanian Ydi",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"gap_lahan_pertanian": 1, "waktu_peralihan_lahan_pertanian": 1},
)
def peralihan_lahan_pertanian_ydi():
    return gap_lahan_pertanian() / waktu_peralihan_lahan_pertanian()


@component.add(
    name="Peralihan Lahan Terbangun Ydi",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"gap_lahan_terbangun": 1, "waktu_peralihan_lahan_terbangun": 1},
)
def peralihan_lahan_terbangun_ydi():
    return gap_lahan_terbangun() / waktu_peralihan_lahan_terbangun()


@component.add(
    name='"Rawa & Badan Air ke Perkebunan Indicated"',
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "peralihan_lahan_perkebunan_ydi": 1,
        "share_rawa_badan_air_ke_perkebunan": 1,
    },
)
def rawa_badan_air_ke_perkebunan_indicated():
    return peralihan_lahan_perkebunan_ydi() * share_rawa_badan_air_ke_perkebunan()


@component.add(
    name="Share Pertambangan ke Lahan Terbangun",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pertambangan_ke_lahan_terbangun_hist": 1,
        "total_peralihan_ke_lahan_terbangun": 1,
    },
)
def share_pertambangan_ke_lahan_terbangun():
    return pertambangan_ke_lahan_terbangun_hist() / total_peralihan_ke_lahan_terbangun()


@component.add(
    name="Share Pertambangan ke Perkebunan",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pertambangan_ke_perkebunan_hist": 1,
        "total_peralihan_ke_perkebunan": 1,
    },
)
def share_pertambangan_ke_perkebunan():
    return pertambangan_ke_perkebunan_hist() / total_peralihan_ke_perkebunan()


@component.add(
    name="Share Pertanian to Lahan Terbangun",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pertanian_to_lahan_terbangun_hist": 1,
        "total_peralihan_ke_lahan_terbangun": 1,
    },
)
def share_pertanian_to_lahan_terbangun():
    return pertanian_to_lahan_terbangun_hist() / total_peralihan_ke_lahan_terbangun()


@component.add(
    name="Total Peralihan ke Lahan Terbangun",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "belukar_padang_rumput_to_lahan_terbangun_hist": 1,
        "hutan_mangrove_to_lahan_terbangun_hist": 1,
        "hutan_primer_hutan_sekunder_to_lahan_terbangun_hist": 1,
        "hutan_tanaman_to_lahan_terbangun_hist": 1,
        "lahan_lainnya_ke_lahan_terbangun_hist": 1,
        "perkebunan_to_lahan_terbangun_hist": 1,
        "pertanian_to_lahan_terbangun_hist": 1,
        "pertambangan_ke_lahan_terbangun_hist": 1,
        "rawa_badan_air_ke_lahan_terbangun_hist": 1,
    },
)
def total_peralihan_ke_lahan_terbangun():
    return (
        belukar_padang_rumput_to_lahan_terbangun_hist()
        + hutan_mangrove_to_lahan_terbangun_hist()
        + hutan_primer_hutan_sekunder_to_lahan_terbangun_hist()
        + hutan_tanaman_to_lahan_terbangun_hist()
        + lahan_lainnya_ke_lahan_terbangun_hist()
        + perkebunan_to_lahan_terbangun_hist()
        + pertanian_to_lahan_terbangun_hist()
        + pertambangan_ke_lahan_terbangun_hist()
        + rawa_badan_air_ke_lahan_terbangun_hist()
    )


@component.add(
    name='"Rawa & Badan Air ke Pertanian Hist"',
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def rawa_badan_air_ke_pertanian_hist():
    return np.interp(time(), [2016, 2017, 2018, 2019], [0, 8796, 0, 537])


@component.add(
    name='"Rawa & Badan Air ke Pertanian Indicated"',
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "peralihan_lahan_pertanian_ydi": 1,
        "share_rawa_badan_air_ke_pertanian": 1,
    },
)
def rawa_badan_air_ke_pertanian_indicated():
    return peralihan_lahan_pertanian_ydi() * share_rawa_badan_air_ke_pertanian()


@component.add(
    name="Total Peralihan ke Pertanian",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "belukar_padang_rumput_to_pertanian_hist": 1,
        "hutan_mangrove_to_pertanian_hist": 1,
        "hutan_primer_hutan_sekunder_to_pertanian_hist": 1,
        "hutan_tanaman_to_pertanian_hist": 1,
        "lahan_lainnya_ke_pertanian_hist": 1,
        "lahan_terbangun_to_pertanian_hist": 1,
        "perkebunan_to_pertanian_hist": 1,
        "pertambangan_ke_pertanian_hist": 1,
        "rawa_badan_air_ke_pertanian_hist": 1,
    },
)
def total_peralihan_ke_pertanian():
    return (
        belukar_padang_rumput_to_pertanian_hist()
        + hutan_mangrove_to_pertanian_hist()
        + hutan_primer_hutan_sekunder_to_pertanian_hist()
        + hutan_tanaman_to_pertanian_hist()
        + lahan_lainnya_ke_pertanian_hist()
        + lahan_terbangun_to_pertanian_hist()
        + perkebunan_to_pertanian_hist()
        + pertambangan_ke_pertanian_hist()
        + rawa_badan_air_ke_pertanian_hist()
    )


@component.add(
    name="Lahan Lainnya ke Pertanian Hist",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def lahan_lainnya_ke_pertanian_hist():
    return np.interp(time(), [2016, 2017, 2018, 2019], [674, 3444, 439, 2579])


@component.add(
    name="Hutan Mangrove to Lahan Terbangun Indicated",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "peralihan_lahan_terbangun_ydi": 1,
        "share_hutan_mangrove_to_lahan_terbangun": 1,
    },
)
def hutan_mangrove_to_lahan_terbangun_indicated():
    return peralihan_lahan_terbangun_ydi() * share_hutan_mangrove_to_lahan_terbangun()


@component.add(
    name='"Hutan Primer & Hutan Sekunder to Perkebunan Hist"',
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def hutan_primer_hutan_sekunder_to_perkebunan_hist():
    return np.interp(time(), [2016, 2017, 2018, 2019], [17736, 40906, 1742, 11062])


@component.add(
    name='"Hutan Primer & Hutan Sekunder to Perkebunan Indicated"',
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "peralihan_lahan_perkebunan_ydi": 1,
        "share_hutan_primer_hutan_sekunder_to_perkebunan": 1,
    },
)
def hutan_primer_hutan_sekunder_to_perkebunan_indicated():
    return (
        peralihan_lahan_perkebunan_ydi()
        * share_hutan_primer_hutan_sekunder_to_perkebunan()
    )


@component.add(
    name="Share Belukar Padang Rumput to Lahan Terbangun",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "belukar_padang_rumput_to_lahan_terbangun_hist": 1,
        "total_peralihan_ke_lahan_terbangun": 1,
    },
)
def share_belukar_padang_rumput_to_lahan_terbangun():
    return (
        belukar_padang_rumput_to_lahan_terbangun_hist()
        / total_peralihan_ke_lahan_terbangun()
    )


@component.add(
    name="Share Belukar Padang Rumput to Perkebunan",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "belukar_padang_rumput_to_perkebunan_hist": 1,
        "total_peralihan_ke_perkebunan": 1,
    },
)
def share_belukar_padang_rumput_to_perkebunan():
    return belukar_padang_rumput_to_perkebunan_hist() / total_peralihan_ke_perkebunan()


@component.add(
    name="Share Belukar Padang Rumput to Pertanian",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "belukar_padang_rumput_to_pertanian_hist": 1,
        "total_peralihan_ke_pertanian": 1,
    },
)
def share_belukar_padang_rumput_to_pertanian():
    return belukar_padang_rumput_to_pertanian_hist() / total_peralihan_ke_pertanian()


@component.add(
    name="Share Hutan Mangrove to Lahan Terbangun",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hutan_mangrove_to_lahan_terbangun_hist": 1,
        "total_peralihan_ke_lahan_terbangun": 1,
    },
)
def share_hutan_mangrove_to_lahan_terbangun():
    return (
        hutan_mangrove_to_lahan_terbangun_hist() / total_peralihan_ke_lahan_terbangun()
    )


@component.add(
    name="Kebutuhan Lahan Perkebunan",
    units="Ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"nilai_tambah_perkebunan": 1, "produktivitas_perkebunan": 1},
)
def kebutuhan_lahan_perkebunan():
    return nilai_tambah_perkebunan() / produktivitas_perkebunan()


@component.add(
    name="Waktu Peralihan Lahan Terbangun",
    units="tahun",
    comp_type="Constant",
    comp_subtype="Normal",
)
def waktu_peralihan_lahan_terbangun():
    return 2


@component.add(
    name="Share Hutan Mangrove to Perkebunan",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hutan_mangrove_to_perkebunan_hist": 1,
        "total_peralihan_ke_perkebunan": 1,
    },
)
def share_hutan_mangrove_to_perkebunan():
    return hutan_mangrove_to_perkebunan_hist() / total_peralihan_ke_perkebunan()


@component.add(
    name='"Share Hutan Primer & Hutan Sekunder to Perkebunan"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hutan_primer_hutan_sekunder_to_perkebunan_hist": 1,
        "total_peralihan_ke_perkebunan": 1,
    },
)
def share_hutan_primer_hutan_sekunder_to_perkebunan():
    return (
        hutan_primer_hutan_sekunder_to_perkebunan_hist()
        / total_peralihan_ke_perkebunan()
    )


@component.add(
    name="Perkebunan to Lahan Terbangun Hist",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def perkebunan_to_lahan_terbangun_hist():
    return np.interp(
        time(), [2016, 2017, 2018, 2019, 2020, 2021, 2022], [210, 167, 150, 0, 3, 0, 88]
    )


@component.add(
    name="Perkebunan to Lahan Terbangun Indicated",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "peralihan_lahan_terbangun_ydi": 1,
        "share_perkebunan_to_lahan_terbangun": 1,
    },
)
def perkebunan_to_lahan_terbangun_indicated():
    return peralihan_lahan_terbangun_ydi() * share_perkebunan_to_lahan_terbangun()


@component.add(
    name="Share Hutan Tanaman to Lahan Terbangun",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hutan_tanaman_to_lahan_terbangun_hist": 1,
        "total_peralihan_ke_lahan_terbangun": 1,
    },
)
def share_hutan_tanaman_to_lahan_terbangun():
    return (
        hutan_tanaman_to_lahan_terbangun_hist() / total_peralihan_ke_lahan_terbangun()
    )


@component.add(
    name='"Hutan Primer & Hutan Sekunder to Pertanian Hist"',
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def hutan_primer_hutan_sekunder_to_pertanian_hist():
    return np.interp(time(), [2016, 2017, 2018, 2019], [21631, 47177, 806, 35038])


@component.add(
    name='"Share Hutan Primer & Hutan Sekunder to Pertanian"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hutan_primer_hutan_sekunder_to_pertanian_hist": 1,
        "total_peralihan_ke_pertanian": 1,
    },
)
def share_hutan_primer_hutan_sekunder_to_pertanian():
    return (
        hutan_primer_hutan_sekunder_to_pertanian_hist() / total_peralihan_ke_pertanian()
    )


@component.add(
    name="Lahan Lainnya ke Pertanian Indicated",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "peralihan_lahan_pertanian_ydi": 1,
        "share_lahan_lainnya_ke_pertanian": 1,
    },
)
def lahan_lainnya_ke_pertanian_indicated():
    return peralihan_lahan_pertanian_ydi() * share_lahan_lainnya_ke_pertanian()


@component.add(
    name="Share Lahan Lainnya ke Pertanian",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "lahan_lainnya_ke_pertanian_hist": 1,
        "total_peralihan_ke_pertanian": 1,
    },
)
def share_lahan_lainnya_ke_pertanian():
    return lahan_lainnya_ke_pertanian_hist() / total_peralihan_ke_pertanian()


@component.add(
    name="Share Lahan Terbangun to Perkebunan",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "lahan_terbangun_to_perkebunan_hist": 1,
        "total_peralihan_ke_perkebunan": 1,
    },
)
def share_lahan_terbangun_to_perkebunan():
    return lahan_terbangun_to_perkebunan_hist() / total_peralihan_ke_perkebunan()


@component.add(
    name="Share Lahan Terbangun to Pertanian",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "lahan_terbangun_to_pertanian_hist": 1,
        "total_peralihan_ke_pertanian": 1,
    },
)
def share_lahan_terbangun_to_pertanian():
    return lahan_terbangun_to_pertanian_hist() / total_peralihan_ke_pertanian()


@component.add(
    name="Share Perkebunan to Pertanian",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"perkebunan_to_pertanian_hist": 1, "total_peralihan_ke_pertanian": 1},
)
def share_perkebunan_to_pertanian():
    return perkebunan_to_pertanian_hist() / total_peralihan_ke_pertanian()


@component.add(
    name="Hutan Mangrove to Pertanian Indicated",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "peralihan_lahan_pertanian_ydi": 1,
        "share_hutan_mangrove_to_pertanian": 1,
    },
)
def hutan_mangrove_to_pertanian_indicated():
    return peralihan_lahan_pertanian_ydi() * share_hutan_mangrove_to_pertanian()


@component.add(
    name='"Rawa & Badan Air ke Perkebunan Hist"',
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def rawa_badan_air_ke_perkebunan_hist():
    return np.interp(time(), [2016, 2017, 2018, 2019], [0, 365, 0, 238])


@component.add(
    name="Hutan Tanaman to Perkebunan Hist",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def hutan_tanaman_to_perkebunan_hist():
    return np.interp(time(), [2016, 2017, 2018, 2019], [0, 0, 0, 0])


@component.add(
    name="Share Pertanian to Perkebunan",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pertanian_to_perkebunan_hist": 1, "total_peralihan_ke_perkebunan": 1},
)
def share_pertanian_to_perkebunan():
    return pertanian_to_perkebunan_hist() / total_peralihan_ke_perkebunan()


@component.add(
    name="Pertambangan ke Pertanian Indicated",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "peralihan_lahan_pertanian_ydi": 1,
        "share_pertambangan_ke_pertanian": 1,
    },
)
def pertambangan_ke_pertanian_indicated():
    return peralihan_lahan_pertanian_ydi() * share_pertambangan_ke_pertanian()


@component.add(
    name="Lahan Lainnya ke Lahan Terbangun Indicated",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "peralihan_lahan_terbangun_ydi": 1,
        "share_lahan_lainnya_ke_lahan_terbangun": 1,
    },
)
def lahan_lainnya_ke_lahan_terbangun_indicated():
    return peralihan_lahan_terbangun_ydi() * share_lahan_lainnya_ke_lahan_terbangun()


@component.add(
    name='"Rawa & Badan Air ke Lahan Terbangun Indicated"',
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "peralihan_lahan_terbangun_ydi": 1,
        "share_rawa_badan_air_ke_lahan_terbangun": 1,
    },
)
def rawa_badan_air_ke_lahan_terbangun_indicated():
    return peralihan_lahan_terbangun_ydi() * share_rawa_badan_air_ke_lahan_terbangun()


@component.add(
    name="Pertanian to Perkebunan Indicated",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "peralihan_lahan_perkebunan_ydi": 1,
        "share_pertanian_to_perkebunan": 1,
    },
)
def pertanian_to_perkebunan_indicated():
    return peralihan_lahan_perkebunan_ydi() * share_pertanian_to_perkebunan()


@component.add(
    name="Pertambangan ke Perkebunan Indicated",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "peralihan_lahan_perkebunan_ydi": 1,
        "share_pertambangan_ke_perkebunan": 1,
    },
)
def pertambangan_ke_perkebunan_indicated():
    return peralihan_lahan_perkebunan_ydi() * share_pertambangan_ke_perkebunan()


@component.add(
    name="Lahan Lainnya ke Perkebunan Indicated",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "peralihan_lahan_perkebunan_ydi": 1,
        "share_lahan_lainnya_ke_perkebunan": 1,
    },
)
def lahan_lainnya_ke_perkebunan_indicated():
    return peralihan_lahan_perkebunan_ydi() * share_lahan_lainnya_ke_perkebunan()


@component.add(
    name="Hutan Mangrove to Perkebunan Hist",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def hutan_mangrove_to_perkebunan_hist():
    return np.interp(time(), [2016, 2017, 2018, 2019], [25, 14, 0, 6])


@component.add(
    name='"Share Hutan Primer & Hutan Sekunder to Lahan Terbangun"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hutan_primer_hutan_sekunder_to_lahan_terbangun_hist": 1,
        "total_peralihan_ke_lahan_terbangun": 1,
    },
)
def share_hutan_primer_hutan_sekunder_to_lahan_terbangun():
    return (
        hutan_primer_hutan_sekunder_to_lahan_terbangun_hist()
        / total_peralihan_ke_lahan_terbangun()
    )


@component.add(
    name="Pertambangan ke Perkebunan Hist",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def pertambangan_ke_perkebunan_hist():
    return np.interp(time(), [2016, 2017, 2018, 2019], [377, 0, 0, 0])


@component.add(
    name="Lahan Lainnya ke Lahan Terbangun Hist",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def lahan_lainnya_ke_lahan_terbangun_hist():
    return np.interp(
        time(), [2016, 2017, 2018, 2019, 2020, 2021, 2022], [6, 0, 45, 16, 46, 0, 19]
    )


@component.add(
    name="Hutan Mangrove to Pertanian Hist",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def hutan_mangrove_to_pertanian_hist():
    return np.interp(time(), [2016, 2017, 2018, 2019], [44, 916, 0, 157])


@component.add(
    name="Pertanian to Lahan Terbangun Hist",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def pertanian_to_lahan_terbangun_hist():
    return np.interp(
        time(),
        [2016, 2017, 2018, 2019, 2020, 2021, 2022],
        [4260, 1714, 6995, 77, 9830, 88, 3827],
    )


@component.add(
    name="Pertambangan ke Pertanian Hist",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def pertambangan_ke_pertanian_hist():
    return np.interp(time(), [2016, 2017, 2018, 2019], [113, 1, 0, 69])


@component.add(
    name="Lahan Lainnya ke Perkebunan Hist",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def lahan_lainnya_ke_perkebunan_hist():
    return np.interp(time(), [2016, 2017, 2018, 2019], [17080, 19944, 4885, 12018])


@component.add(
    name="Hutan Mangrove to Perkebunan Indicated",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "peralihan_lahan_perkebunan_ydi": 1,
        "share_hutan_mangrove_to_perkebunan": 1,
    },
)
def hutan_mangrove_to_perkebunan_indicated():
    return peralihan_lahan_perkebunan_ydi() * share_hutan_mangrove_to_perkebunan()


@component.add(
    name="Lahan Terbangun per Kapita Init",
    units="Ha/jiwa",
    comp_type="Constant",
    comp_subtype="Normal",
)
def lahan_terbangun_per_kapita_init():
    return 0.017


@component.add(
    name="Share Lahan Lainnya ke Perkebunan",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "lahan_lainnya_ke_perkebunan_hist": 1,
        "total_peralihan_ke_perkebunan": 1,
    },
)
def share_lahan_lainnya_ke_perkebunan():
    return lahan_lainnya_ke_perkebunan_hist() / total_peralihan_ke_perkebunan()


@component.add(
    name='"Rawa & Badan Air ke Lahan Terbangun Hist"',
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def rawa_badan_air_ke_lahan_terbangun_hist():
    return np.interp(
        time(), [2016, 2017, 2018, 2019, 2020, 2021, 2022], [3, 2, 0, 0, 24, 0, 5]
    )


@component.add(
    name="Waktu Peralihan Lahan Pertanian",
    units="tahun",
    comp_type="Constant",
    comp_subtype="Normal",
)
def waktu_peralihan_lahan_pertanian():
    return 2


@component.add(
    name="Hutan Tanaman to Lahan Terbangun Indicated",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "peralihan_lahan_terbangun_ydi": 1,
        "share_hutan_tanaman_to_lahan_terbangun": 1,
    },
)
def hutan_tanaman_to_lahan_terbangun_indicated():
    return peralihan_lahan_terbangun_ydi() * share_hutan_tanaman_to_lahan_terbangun()


@component.add(
    name="Perubahan Nilai Tambah Perkebunan",
    units="JutaRp/(tahun*tahun)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fraksi_perubahan_nilai_tambah_perkebunan": 1,
        "nilai_tambah_perkebunan": 1,
    },
)
def perubahan_nilai_tambah_perkebunan():
    return fraksi_perubahan_nilai_tambah_perkebunan() * nilai_tambah_perkebunan()


@component.add(
    name="Waktu Peralihan Lahan Perkebunan",
    units="tahun",
    comp_type="Constant",
    comp_subtype="Normal",
)
def waktu_peralihan_lahan_perkebunan():
    return 2


@component.add(
    name="Share Hutan Mangrove to Pertanian",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hutan_mangrove_to_pertanian_hist": 1,
        "total_peralihan_ke_pertanian": 1,
    },
)
def share_hutan_mangrove_to_pertanian():
    return hutan_mangrove_to_pertanian_hist() / total_peralihan_ke_pertanian()


@component.add(
    name="Share Lahan Lainnya ke Lahan Terbangun",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "lahan_lainnya_ke_lahan_terbangun_hist": 1,
        "total_peralihan_ke_lahan_terbangun": 1,
    },
)
def share_lahan_lainnya_ke_lahan_terbangun():
    return (
        lahan_lainnya_ke_lahan_terbangun_hist() / total_peralihan_ke_lahan_terbangun()
    )


@component.add(
    name='"Hutan Primer & Hutan Sekunder to Pertanian Indicated"',
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "peralihan_lahan_pertanian_ydi": 1,
        "share_hutan_primer_hutan_sekunder_to_pertanian": 1,
    },
)
def hutan_primer_hutan_sekunder_to_pertanian_indicated():
    return (
        peralihan_lahan_pertanian_ydi()
        * share_hutan_primer_hutan_sekunder_to_pertanian()
    )


@component.add(
    name="Pertanian ke Lahan Lainnya",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "availability_effect_pertanian": 1,
        "pertanian_ke_lahan_lainnya_share": 1,
        "pertanian": 1,
    },
)
def pertanian_ke_lahan_lainnya():
    return (
        availability_effect_pertanian()
        * pertanian_ke_lahan_lainnya_share()
        * pertanian()
    )


@component.add(
    name="Lahan Terbangun ke Lahan Lainnya",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "availability_effect_lahan_terbangun": 1,
        "lahan_terbangun_ke_lahan_lainnya_share": 1,
        "lahan_terbangun": 1,
    },
)
def lahan_terbangun_ke_lahan_lainnya():
    return (
        availability_effect_lahan_terbangun()
        * lahan_terbangun_ke_lahan_lainnya_share()
        * lahan_terbangun()
    )


@component.add(
    name="Pertanian ke Pertambangan",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pertanian_ke_pertambangan_share": 1,
        "availability_effect_pertanian": 1,
        "pertanian": 1,
    },
)
def pertanian_ke_pertambangan():
    return (
        pertanian_ke_pertambangan_share()
        * availability_effect_pertanian()
        * pertanian()
    )


@component.add(
    name="Lahan Terbangun ke Pertambangan",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "lahan_terbangun_ke_pertambangan_share": 1,
        "availability_effect_lahan_terbangun": 1,
        "lahan_terbangun": 1,
    },
)
def lahan_terbangun_ke_pertambangan():
    return (
        lahan_terbangun_ke_pertambangan_share()
        * availability_effect_lahan_terbangun()
        * lahan_terbangun()
    )


@component.add(
    name='"Pertanian ke Rawa & Badan Air"',
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pertanian_ke_rawa_badan_air_share": 1,
        "availability_effect_pertanian": 1,
        "pertanian": 1,
    },
)
def pertanian_ke_rawa_badan_air():
    return (
        pertanian_ke_rawa_badan_air_share()
        * availability_effect_pertanian()
        * pertanian()
    )


@component.add(
    name='"Lahan Terbangun ke Rawa & Badan Air"',
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "availability_effect_lahan_terbangun": 1,
        "lahan_terbangun_ke_rawa_badan_air_share": 1,
        "lahan_terbangun": 1,
    },
)
def lahan_terbangun_ke_rawa_badan_air():
    return (
        availability_effect_lahan_terbangun()
        * lahan_terbangun_ke_rawa_badan_air_share()
        * lahan_terbangun()
    )


@component.add(
    name='"Pertambangan ke Hutan Primer & Sekunder"',
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pertambangan_ke_hutan_primer_sekunder_share": 1,
        "availability_effect_pertambangan": 1,
        "pertambangan": 1,
    },
)
def pertambangan_ke_hutan_primer_sekunder():
    return (
        pertambangan_ke_hutan_primer_sekunder_share()
        * availability_effect_pertambangan()
        * pertambangan()
    )


@component.add(
    name='"Perkebunan ke Rawa & Badan Air"',
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "perkebunan_ke_rawa_badan_air_share": 1,
        "availability_effect_perkebunan": 1,
        "perkebunan": 1,
    },
)
def perkebunan_ke_rawa_badan_air():
    return (
        perkebunan_ke_rawa_badan_air_share()
        * availability_effect_perkebunan()
        * perkebunan()
    )


@component.add(
    name="Lahan Terbangun to Belukar Padang Rumput",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "lahan_terbangun_to_belukar_padang_rumput_share": 1,
        "availability_effect_lahan_terbangun": 1,
        "lahan_terbangun": 1,
    },
)
def lahan_terbangun_to_belukar_padang_rumput():
    return (
        lahan_terbangun_to_belukar_padang_rumput_share()
        * availability_effect_lahan_terbangun()
        * lahan_terbangun()
    )


@component.add(
    name="Pertanian to Belukar Padang Rumput",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pertanian_to_belukar_padang_rumput_share": 1,
        "availability_effect_pertanian": 1,
        "pertanian": 1,
    },
)
def pertanian_to_belukar_padang_rumput():
    return (
        pertanian_to_belukar_padang_rumput_share()
        * availability_effect_pertanian()
        * pertanian()
    )


@component.add(
    name="Lahan Terbangun to Hutan Mangrove",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "lahan_terbangun_to_hutan_mangrove_share": 1,
        "availability_effect_lahan_terbangun": 1,
        "lahan_terbangun": 1,
    },
)
def lahan_terbangun_to_hutan_mangrove():
    return (
        lahan_terbangun_to_hutan_mangrove_share()
        * availability_effect_lahan_terbangun()
        * lahan_terbangun()
    )


@component.add(
    name="Pertanian to Hutan Mangrove",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pertanian_to_hutan_mangrove_share": 1,
        "availability_effect_pertanian": 1,
        "pertanian": 1,
    },
)
def pertanian_to_hutan_mangrove():
    return (
        pertanian_to_hutan_mangrove_share()
        * availability_effect_pertanian()
        * pertanian()
    )


@component.add(
    name="Perkebunan to Hutan Mangrove",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "perkebunan_to_hutan_mangrove_share": 1,
        "availability_effect_perkebunan": 1,
        "perkebunan": 1,
    },
)
def perkebunan_to_hutan_mangrove():
    return (
        perkebunan_to_hutan_mangrove_share()
        * availability_effect_perkebunan()
        * perkebunan()
    )


@component.add(
    name='"Lahan Terbangun to Hutan Primer & Sekunder"',
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "lahan_terbangun_to_hutan_primer_sekunder_share": 1,
        "availability_effect_lahan_terbangun": 1,
        "lahan_terbangun": 1,
    },
)
def lahan_terbangun_to_hutan_primer_sekunder():
    return (
        lahan_terbangun_to_hutan_primer_sekunder_share()
        * availability_effect_lahan_terbangun()
        * lahan_terbangun()
    )


@component.add(
    name="Lahan Terbangun to Hutan Tanaman",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "lahan_terbangun_to_hutan_tanaman_share": 1,
        "availability_effect_lahan_terbangun": 1,
        "lahan_terbangun": 1,
    },
)
def lahan_terbangun_to_hutan_tanaman():
    return (
        lahan_terbangun_to_hutan_tanaman_share()
        * availability_effect_lahan_terbangun()
        * lahan_terbangun()
    )


@component.add(
    name="Pertanian to Hutan Tanaman",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pertanian_to_hutan_tanaman_share": 1,
        "availability_effect_pertanian": 1,
        "pertanian": 1,
    },
)
def pertanian_to_hutan_tanaman():
    return (
        pertanian_to_hutan_tanaman_share()
        * availability_effect_pertanian()
        * pertanian()
    )


@component.add(
    name="Lahan Terbangun to Perkebunan",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "lahan_terbangun_to_perkebunan_share": 1,
        "availability_effect_lahan_terbangun": 1,
        "lahan_terbangun": 1,
    },
)
def lahan_terbangun_to_perkebunan():
    return (
        lahan_terbangun_to_perkebunan_share()
        * availability_effect_lahan_terbangun()
        * lahan_terbangun()
    )


@component.add(
    name="Lahan Terbangun to Pertanian",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "lahan_terbangun_to_pertanian_share": 1,
        "availability_effect_lahan_terbangun": 1,
        "lahan_terbangun": 1,
    },
)
def lahan_terbangun_to_pertanian():
    return (
        lahan_terbangun_to_pertanian_share()
        * availability_effect_lahan_terbangun()
        * lahan_terbangun()
    )


@component.add(
    name="Pertanian to Perkebunan",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pertanian_to_perkebunan_share": 1,
        "availability_effect_pertanian": 1,
        "pertanian": 1,
    },
)
def pertanian_to_perkebunan():
    return (
        pertanian_to_perkebunan_share() * availability_effect_pertanian() * pertanian()
    )


@component.add(
    name="Belukar Padang Rumput ke Lahan Lainnya",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "availability_effect_belukar_padang_rumput": 1,
        "belukar_padang_rumput_ke_lahan_lainnya_share": 1,
        "belukar_padang_rumput": 1,
    },
)
def belukar_padang_rumput_ke_lahan_lainnya():
    return (
        availability_effect_belukar_padang_rumput()
        * belukar_padang_rumput_ke_lahan_lainnya_share()
        * belukar_padang_rumput()
    )


@component.add(
    name='"Rawa & Badan Air ke Hutan Mangrove"',
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "rawa_badan_air_ke_hutan_mangrove_share": 1,
        "availability_effect_rawa_badan_air": 1,
        "rawa_badan_air": 1,
    },
)
def rawa_badan_air_ke_hutan_mangrove():
    return (
        rawa_badan_air_ke_hutan_mangrove_share()
        * availability_effect_rawa_badan_air()
        * rawa_badan_air()
    )


@component.add(
    name="Belukar Padang Rumput ke Pertambangan",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "belukar_padang_rumput_ke_pertambangan_share": 1,
        "availability_effect_belukar_padang_rumput": 1,
        "belukar_padang_rumput": 1,
    },
)
def belukar_padang_rumput_ke_pertambangan():
    return (
        belukar_padang_rumput_ke_pertambangan_share()
        * availability_effect_belukar_padang_rumput()
        * belukar_padang_rumput()
    )


@component.add(
    name="Perkebunan to Belukar Padang Rumput",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "perkebunan_to_belukar_padang_rumput_share": 1,
        "availability_effect_perkebunan": 1,
        "perkebunan": 1,
    },
)
def perkebunan_to_belukar_padang_rumput():
    return (
        perkebunan_to_belukar_padang_rumput_share()
        * availability_effect_perkebunan()
        * perkebunan()
    )


@component.add(
    name="Lahan Lainnya ke Belukar Padang Rumput",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "availability_effect_lahan_lainnya": 1,
        "lahan_lainnya_ke_belukar_padang_rumput_share": 1,
        "lahan_lainnya": 1,
    },
)
def lahan_lainnya_ke_belukar_padang_rumput():
    return (
        availability_effect_lahan_lainnya()
        * lahan_lainnya_ke_belukar_padang_rumput_share()
        * lahan_lainnya()
    )


@component.add(
    name='"Belukar Padang Rumput ke Rawa & Badan Air"',
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "belukar_padang_rumput_ke_rawa_badan_air_share": 1,
        "availability_effect_belukar_padang_rumput": 1,
        "belukar_padang_rumput": 1,
    },
)
def belukar_padang_rumput_ke_rawa_badan_air():
    return (
        belukar_padang_rumput_ke_rawa_badan_air_share()
        * availability_effect_belukar_padang_rumput()
        * belukar_padang_rumput()
    )


@component.add(
    name="Belukar Padang Rumput to Hutan Mangrove",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "belukar_padang_rumput_to_hutan_mangrove_share": 1,
        "availability_effect_belukar_padang_rumput": 1,
        "belukar_padang_rumput": 1,
    },
)
def belukar_padang_rumput_to_hutan_mangrove():
    return (
        belukar_padang_rumput_to_hutan_mangrove_share()
        * availability_effect_belukar_padang_rumput()
        * belukar_padang_rumput()
    )


@component.add(
    name="Perkebunan ke Lahan Lainnya",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "availability_effect_perkebunan": 1,
        "perkebunan_ke_lahan_lainnya_share": 1,
        "perkebunan": 1,
    },
)
def perkebunan_ke_lahan_lainnya():
    return (
        availability_effect_perkebunan()
        * perkebunan_ke_lahan_lainnya_share()
        * perkebunan()
    )


@component.add(
    name="Pertambangan ke Hutan Mangrove",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pertambangan_ke_hutan_mangrove_share": 1,
        "availability_effect_pertambangan": 1,
        "pertambangan": 1,
    },
)
def pertambangan_ke_hutan_mangrove():
    return (
        pertambangan_ke_hutan_mangrove_share()
        * availability_effect_pertambangan()
        * pertambangan()
    )


@component.add(
    name='"Belukar Padang Rumput to Hutan Primer & Sekunder"',
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "belukar_padang_rumput_to_hutan_primer_sekunder_share": 1,
        "availability_effect_belukar_padang_rumput": 1,
        "belukar_padang_rumput": 1,
    },
)
def belukar_padang_rumput_to_hutan_primer_sekunder():
    return (
        belukar_padang_rumput_to_hutan_primer_sekunder_share()
        * availability_effect_belukar_padang_rumput()
        * belukar_padang_rumput()
    )


@component.add(
    name="Belukar Padang Rumput to Hutan Tanaman",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "belukar_padang_rumput_to_hutan_tanaman_share": 1,
        "availability_effect_belukar_padang_rumput": 1,
        "belukar_padang_rumput": 1,
    },
)
def belukar_padang_rumput_to_hutan_tanaman():
    return (
        belukar_padang_rumput_to_hutan_tanaman_share()
        * availability_effect_belukar_padang_rumput()
        * belukar_padang_rumput()
    )


@component.add(
    name='"Rawa & Badan Air ke Belukar Padang Rumput"',
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "rawa_badan_air_ke_belukar_padang_rumput_share": 1,
        "availability_effect_rawa_badan_air": 1,
        "rawa_badan_air": 1,
    },
)
def rawa_badan_air_ke_belukar_padang_rumput():
    return (
        rawa_badan_air_ke_belukar_padang_rumput_share()
        * availability_effect_rawa_badan_air()
        * rawa_badan_air()
    )


@component.add(
    name='"Rawa & Badan Air ke Pertambangan"',
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "rawa_badan_air_ke_pertambangan_share": 1,
        "availability_effect_rawa_badan_air": 1,
        "rawa_badan_air": 1,
    },
)
def rawa_badan_air_ke_pertambangan():
    return (
        rawa_badan_air_ke_pertambangan_share()
        * availability_effect_rawa_badan_air()
        * rawa_badan_air()
    )


@component.add(
    name="Belukar Padang Rumput to Perkebunan",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "belukar_padang_rumput_to_perkebunan_share": 1,
        "availability_effect_belukar_padang_rumput": 1,
        "belukar_padang_rumput": 1,
    },
)
def belukar_padang_rumput_to_perkebunan():
    return (
        belukar_padang_rumput_to_perkebunan_share()
        * availability_effect_belukar_padang_rumput()
        * belukar_padang_rumput()
    )


@component.add(
    name='"Rawa & Badan Air ke Hutan Primer & Sekunder"',
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "availability_effect_rawa_badan_air": 1,
        "rawa_badan_air_ke_hutan_primer_sekunder_share": 1,
        "rawa_badan_air": 1,
    },
)
def rawa_badan_air_ke_hutan_primer_sekunder():
    return (
        availability_effect_rawa_badan_air()
        * rawa_badan_air_ke_hutan_primer_sekunder_share()
        * rawa_badan_air()
    )


@component.add(
    name="Belukar Padang Rumput to Pertanian",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "belukar_padang_rumput_to_pertanian_share": 1,
        "availability_effect_belukar_padang_rumput": 1,
        "belukar_padang_rumput": 1,
    },
)
def belukar_padang_rumput_to_pertanian():
    return (
        belukar_padang_rumput_to_pertanian_share()
        * availability_effect_belukar_padang_rumput()
        * belukar_padang_rumput()
    )


@component.add(
    name='"Rawa & Badan Air ke Hutan Tanaman"',
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "rawa_badan_air_ke_hutan_tanaman_share": 1,
        "availability_effect_rawa_badan_air": 1,
        "rawa_badan_air": 1,
    },
)
def rawa_badan_air_ke_hutan_tanaman():
    return (
        rawa_badan_air_ke_hutan_tanaman_share()
        * availability_effect_rawa_badan_air()
        * rawa_badan_air()
    )


@component.add(
    name="Pertambangan ke Perkebunan",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pertambangan_ke_perkebunan_share": 1,
        "availability_effect_pertambangan": 1,
        "pertambangan": 1,
    },
)
def pertambangan_ke_perkebunan():
    return (
        pertambangan_ke_perkebunan_share()
        * availability_effect_pertambangan()
        * pertambangan()
    )


@component.add(
    name='"Pertanian to Hutan Primer & Sekunder"',
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pertanian_to_hutan_primer_sekunder_share": 1,
        "availability_effect_pertanian": 1,
        "pertanian": 1,
    },
)
def pertanian_to_hutan_primer_sekunder():
    return (
        pertanian_to_hutan_primer_sekunder_share()
        * availability_effect_pertanian()
        * pertanian()
    )


@component.add(
    name="Pertambangan ke Pertanian",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pertambangan_ke_pertanian_share": 1,
        "availability_effect_pertambangan": 1,
        "pertambangan": 1,
    },
)
def pertambangan_ke_pertanian():
    return (
        pertambangan_ke_pertanian_share()
        * availability_effect_pertambangan()
        * pertambangan()
    )


@component.add(
    name='"Lahan Lainnya ke Rawa & Badan Air"',
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "availability_effect_lahan_lainnya": 1,
        "lahan_lainnya_ke_rawa_badan_air_share": 1,
        "lahan_lainnya": 1,
    },
)
def lahan_lainnya_ke_rawa_badan_air():
    return (
        availability_effect_lahan_lainnya()
        * lahan_lainnya_ke_rawa_badan_air_share()
        * lahan_lainnya()
    )


@component.add(
    name="Perkebunan ke Pertambangan",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "perkebunan_ke_pertambangan_share": 1,
        "availability_effect_perkebunan": 1,
        "perkebunan": 1,
    },
)
def perkebunan_ke_pertambangan():
    return (
        perkebunan_ke_pertambangan_share()
        * availability_effect_perkebunan()
        * perkebunan()
    )


@component.add(
    name='"Rawa & Badan Air ke Perkebunan"',
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "rawa_badan_air_ke_perkebunan_share": 1,
        "availability_effect_rawa_badan_air": 1,
        "rawa_badan_air": 1,
    },
)
def rawa_badan_air_ke_perkebunan():
    return (
        rawa_badan_air_ke_perkebunan_share()
        * availability_effect_rawa_badan_air()
        * rawa_badan_air()
    )


@component.add(
    name='"Pertambangan ke Rawa & Badan Air"',
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pertambangan_ke_rawa_badan_air_share": 1,
        "availability_effect_pertambangan": 1,
        "pertambangan": 1,
    },
)
def pertambangan_ke_rawa_badan_air():
    return (
        pertambangan_ke_rawa_badan_air_share()
        * availability_effect_pertambangan()
        * pertambangan()
    )


@component.add(
    name="Perkebunan to Pertanian",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "perkebunan_to_pertanian_share": 1,
        "availability_effect_perkebunan": 1,
        "perkebunan": 1,
    },
)
def perkebunan_to_pertanian():
    return (
        perkebunan_to_pertanian_share()
        * availability_effect_perkebunan()
        * perkebunan()
    )


@component.add(
    name='"Rawa & Badan Air ke Pertanian"',
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "rawa_badan_air_ke_pertanian_share": 1,
        "availability_effect_rawa_badan_air": 1,
        "rawa_badan_air": 1,
    },
)
def rawa_badan_air_ke_pertanian():
    return (
        rawa_badan_air_ke_pertanian_share()
        * availability_effect_rawa_badan_air()
        * rawa_badan_air()
    )


@component.add(
    name="Pertambangan ke Lahan Lainnya",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "availability_effect_pertambangan": 1,
        "pertambangan_ke_lahan_lainnya_share": 1,
        "pertambangan": 1,
    },
)
def pertambangan_ke_lahan_lainnya():
    return (
        availability_effect_pertambangan()
        * pertambangan_ke_lahan_lainnya_share()
        * pertambangan()
    )


@component.add(
    name="Hutan Tanaman to Hutan Mangrove",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hutan_tanaman_to_hutan_mangrove_share": 1,
        "availability_effect_hutan_tanaman": 1,
        "hutan_tanaman": 1,
    },
)
def hutan_tanaman_to_hutan_mangrove():
    return (
        hutan_tanaman_to_hutan_mangrove_share()
        * availability_effect_hutan_tanaman()
        * hutan_tanaman()
    )


@component.add(
    name='"Rawa & Badan Air ke Lahan Lainnya"',
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "availability_effect_rawa_badan_air": 1,
        "rawa_badan_air_ke_lahan_lainnya_share": 1,
        "rawa_badan_air": 1,
    },
)
def rawa_badan_air_ke_lahan_lainnya():
    return (
        availability_effect_rawa_badan_air()
        * rawa_badan_air_ke_lahan_lainnya_share()
        * rawa_badan_air()
    )


@component.add(
    name="Pertambangan ke Belukar Padang Rumput",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pertambangan_ke_belukar_padang_rumput_share": 1,
        "availability_effect_pertambangan": 1,
        "pertambangan": 1,
    },
)
def pertambangan_ke_belukar_padang_rumput():
    return (
        pertambangan_ke_belukar_padang_rumput_share()
        * availability_effect_pertambangan()
        * pertambangan()
    )


@component.add(
    name='"Perkebunan to Hutan Primer & Sekunder"',
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "perkebunan_to_hutan_primer_sekunder_share": 1,
        "availability_effect_perkebunan": 1,
        "perkebunan": 1,
    },
)
def perkebunan_to_hutan_primer_sekunder():
    return (
        perkebunan_to_hutan_primer_sekunder_share()
        * availability_effect_perkebunan()
        * perkebunan()
    )


@component.add(
    name="Perkebunan to Hutan Tanaman",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "perkebunan_to_hutan_tanamang_share": 1,
        "availability_effect_perkebunan": 1,
        "perkebunan": 1,
    },
)
def perkebunan_to_hutan_tanaman():
    return (
        perkebunan_to_hutan_tanamang_share()
        * availability_effect_perkebunan()
        * perkebunan()
    )


@component.add(
    name='"Lahan Lainnya ke Hutan Primer & Sekunder"',
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "availability_effect_lahan_lainnya": 1,
        "lahan_lainnya_ke_hutan_primer_sekunder_share": 1,
        "lahan_lainnya": 1,
    },
)
def lahan_lainnya_ke_hutan_primer_sekunder():
    return (
        availability_effect_lahan_lainnya()
        * lahan_lainnya_ke_hutan_primer_sekunder_share()
        * lahan_lainnya()
    )


@component.add(
    name="Lahan Lainnya ke Hutan Tanaman",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "availability_effect_lahan_lainnya": 1,
        "lahan_lainnya_ke_hutan_tanamang_share": 1,
        "lahan_lainnya": 1,
    },
)
def lahan_lainnya_ke_hutan_tanaman():
    return (
        availability_effect_lahan_lainnya()
        * lahan_lainnya_ke_hutan_tanamang_share()
        * lahan_lainnya()
    )


@component.add(
    name="Lahan Lainnya ke Pertanian",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "availability_effect_lahan_lainnya": 1,
        "lahan_lainnya_ke_pertanian_share": 1,
        "lahan_lainnya": 1,
    },
)
def lahan_lainnya_ke_pertanian():
    return (
        availability_effect_lahan_lainnya()
        * lahan_lainnya_ke_pertanian_share()
        * lahan_lainnya()
    )


@component.add(
    name="Pertambangan ke Hutan Tanaman",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pertambangan_ke_hutan_tanaman_share": 1,
        "availability_effect_pertambangan": 1,
        "pertambangan": 1,
    },
)
def pertambangan_ke_hutan_tanaman():
    return (
        pertambangan_ke_hutan_tanaman_share()
        * availability_effect_pertambangan()
        * pertambangan()
    )


@component.add(
    name="Lahan Lainnya ke Perkebunan",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "availability_effect_lahan_lainnya": 1,
        "lahan_lainnya_ke_perkebunan_share": 1,
        "lahan_lainnya": 1,
    },
)
def lahan_lainnya_ke_perkebunan():
    return (
        availability_effect_lahan_lainnya()
        * lahan_lainnya_ke_perkebunan_share()
        * lahan_lainnya()
    )


@component.add(
    name="Lahan Lainnya ke Pertambangan",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "availability_effect_lahan_lainnya": 1,
        "lahan_lainnya_ke_pertambangan_share": 1,
        "lahan_lainnya": 1,
    },
)
def lahan_lainnya_ke_pertambangan():
    return (
        availability_effect_lahan_lainnya()
        * lahan_lainnya_ke_pertambangan_share()
        * lahan_lainnya()
    )


@component.add(
    name="Lahan Lainnya ke Hutan Mangrove",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "availability_effect_lahan_lainnya": 1,
        "lahan_lainnya_ke_hutan_mangrove_share": 1,
        "lahan_lainnya": 1,
    },
)
def lahan_lainnya_ke_hutan_mangrove():
    return (
        availability_effect_lahan_lainnya()
        * lahan_lainnya_ke_hutan_mangrove_share()
        * lahan_lainnya()
    )


@component.add(
    name='"Hutan Mangrove ke Rawa & Badan Air"',
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hutan_mangrove_ke_rawa_badan_air_share": 1,
        "availability_effect_hutan_mangrove": 1,
        "hutan_mangrove": 1,
    },
)
def hutan_mangrove_ke_rawa_badan_air():
    return (
        hutan_mangrove_ke_rawa_badan_air_share()
        * availability_effect_hutan_mangrove()
        * hutan_mangrove()
    )


@component.add(
    name="Hutan Tanaman to Perkebunan",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hutan_tanaman_to_perkebunan_share": 1,
        "availability_effect_hutan_tanaman": 1,
        "hutan_tanaman": 1,
    },
)
def hutan_tanaman_to_perkebunan():
    return (
        hutan_tanaman_to_perkebunan_share()
        * availability_effect_hutan_tanaman()
        * hutan_tanaman()
    )


@component.add(
    name="Hutan Tanaman ke Pertambangan",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hutan_tanaman_ke_pertambangan_share": 1,
        "availability_effect_hutan_tanaman": 1,
        "hutan_tanaman": 1,
    },
)
def hutan_tanaman_ke_pertambangan():
    return (
        hutan_tanaman_ke_pertambangan_share()
        * availability_effect_hutan_tanaman()
        * hutan_tanaman()
    )


@component.add(
    name="Hutan Tanaman to Pertanian",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hutan_tanaman_to_pertanian_share": 1,
        "availability_effect_hutan_tanaman": 1,
        "hutan_tanaman": 1,
    },
)
def hutan_tanaman_to_pertanian():
    return (
        hutan_tanaman_to_pertanian_share()
        * availability_effect_hutan_tanaman()
        * hutan_tanaman()
    )


@component.add(
    name='"Hutan Mangrove to Hutan Primer & Sekunder"',
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hutan_mangrove_to_hutan_primer_sekunder_share": 1,
        "availability_effect_hutan_mangrove": 1,
        "hutan_mangrove": 1,
    },
)
def hutan_mangrove_to_hutan_primer_sekunder():
    return (
        hutan_mangrove_to_hutan_primer_sekunder_share()
        * availability_effect_hutan_mangrove()
        * hutan_mangrove()
    )


@component.add(
    name="Hutan Mangrove to Hutan Tanaman",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hutan_mangrove_to_hutan_tanamang_share": 1,
        "availability_effect_hutan_mangrove": 1,
        "hutan_mangrove": 1,
    },
)
def hutan_mangrove_to_hutan_tanaman():
    return (
        hutan_mangrove_to_hutan_tanamang_share()
        * availability_effect_hutan_mangrove()
        * hutan_mangrove()
    )


@component.add(
    name="Hutan Tanaman to Belukar Padang Rumput",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hutan_tanaman_to_belukar_padang_rumput_share": 1,
        "availability_effect_hutan_tanaman": 1,
        "hutan_tanaman": 1,
    },
)
def hutan_tanaman_to_belukar_padang_rumput():
    return (
        hutan_tanaman_to_belukar_padang_rumput_share()
        * availability_effect_hutan_tanaman()
        * hutan_tanaman()
    )


@component.add(
    name="Hutan Mangrove ke Lahan Lainnya",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "availability_effect_hutan_mangrove": 1,
        "hutan_mangrove_ke_lahan_lainnya_share": 1,
        "hutan_mangrove": 1,
    },
)
def hutan_mangrove_ke_lahan_lainnya():
    return (
        availability_effect_hutan_mangrove()
        * hutan_mangrove_ke_lahan_lainnya_share()
        * hutan_mangrove()
    )


@component.add(
    name="Hutan Mangrove to Perkebunan",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hutan_mangrove_to_perkebunan_share": 1,
        "availability_effect_hutan_mangrove": 1,
        "hutan_mangrove": 1,
    },
)
def hutan_mangrove_to_perkebunan():
    return (
        hutan_mangrove_to_perkebunan_share()
        * availability_effect_hutan_mangrove()
        * hutan_mangrove()
    )


@component.add(
    name="Hutan Mangrove ke Pertambangan",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hutan_mangrove_ke_pertambangan_share": 1,
        "availability_effect_hutan_mangrove": 1,
        "hutan_mangrove": 1,
    },
)
def hutan_mangrove_ke_pertambangan():
    return (
        hutan_mangrove_ke_pertambangan_share()
        * availability_effect_hutan_mangrove()
        * hutan_mangrove()
    )


@component.add(
    name="Hutan Mangrove to Pertanian",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hutan_mangrove_to_pertanian_share": 1,
        "availability_effect_hutan_mangrove": 1,
        "hutan_mangrove": 1,
    },
)
def hutan_mangrove_to_pertanian():
    return (
        hutan_mangrove_to_pertanian_share()
        * availability_effect_hutan_mangrove()
        * hutan_mangrove()
    )


@component.add(
    name="Hutan Tanaman ke Lahan Lainnya",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "availability_effect_hutan_tanaman": 1,
        "hutan_tanaman_ke_lahan_lainnya_share": 1,
        "hutan_tanaman": 1,
    },
)
def hutan_tanaman_ke_lahan_lainnya():
    return (
        availability_effect_hutan_tanaman()
        * hutan_tanaman_ke_lahan_lainnya_share()
        * hutan_tanaman()
    )


@component.add(
    name='"Hutan Primer & Hutan Sekunder ke Lahan Lainnya"',
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "availability_effect_hutan_primer_sekunder": 1,
        "hutan_primer_sekunder_ke_lahan_lainnya_share": 1,
        "hutan_primer_sekunder": 1,
    },
)
def hutan_primer_hutan_sekunder_ke_lahan_lainnya():
    return (
        availability_effect_hutan_primer_sekunder()
        * hutan_primer_sekunder_ke_lahan_lainnya_share()
        * hutan_primer_sekunder()
    )


@component.add(
    name="Hutan Mangrove to Belukar Padang Rumput",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hutan_mangrove_to_belukar_padang_rumput_share": 1,
        "availability_effect_hutan_mangrove": 1,
        "hutan_mangrove": 1,
    },
)
def hutan_mangrove_to_belukar_padang_rumput():
    return (
        hutan_mangrove_to_belukar_padang_rumput_share()
        * availability_effect_hutan_mangrove()
        * hutan_mangrove()
    )


@component.add(
    name='"Hutan Primer & Hutan Sekunder to Belukar Padang Rumput"',
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hutan_primer_sekunder_to_belukar_padang_rumput_share": 1,
        "availability_effect_hutan_primer_sekunder": 1,
        "hutan_primer_sekunder": 1,
    },
)
def hutan_primer_hutan_sekunder_to_belukar_padang_rumput():
    return (
        hutan_primer_sekunder_to_belukar_padang_rumput_share()
        * availability_effect_hutan_primer_sekunder()
        * hutan_primer_sekunder()
    )


@component.add(
    name='"Hutan Primer & Hutan Sekunder to Hutan Mangrove"',
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "availability_effect_hutan_primer_sekunder": 1,
        "hutan_primer_sekunder_to_hutan_mangrove_share": 1,
        "hutan_primer_sekunder": 1,
    },
)
def hutan_primer_hutan_sekunder_to_hutan_mangrove():
    return (
        availability_effect_hutan_primer_sekunder()
        * hutan_primer_sekunder_to_hutan_mangrove_share()
        * hutan_primer_sekunder()
    )


@component.add(
    name='"Hutan Tanaman ke Rawa & Badan Air"',
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hutan_tanaman_ke_rawa_badan_air_share": 1,
        "availability_effect_hutan_tanaman": 1,
        "hutan_tanaman": 1,
    },
)
def hutan_tanaman_ke_rawa_badan_air():
    return (
        hutan_tanaman_ke_rawa_badan_air_share()
        * availability_effect_hutan_tanaman()
        * hutan_tanaman()
    )


@component.add(
    name='"Hutan Primer & Hutan Sekunder to Hutan Tanaman"',
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hutan_primer_sekunder_to_hutan_tanaman_share": 1,
        "availability_effect_hutan_primer_sekunder": 1,
        "hutan_primer_sekunder": 1,
    },
)
def hutan_primer_hutan_sekunder_to_hutan_tanaman():
    return (
        hutan_primer_sekunder_to_hutan_tanaman_share()
        * availability_effect_hutan_primer_sekunder()
        * hutan_primer_sekunder()
    )


@component.add(
    name='"Hutan Primer & Hutan Sekunder to Perkebunan"',
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hutan_primer_sekunder_to_perkebunan_share": 1,
        "availability_effect_hutan_primer_sekunder": 1,
        "hutan_primer_sekunder": 1,
    },
)
def hutan_primer_hutan_sekunder_to_perkebunan():
    return (
        hutan_primer_sekunder_to_perkebunan_share()
        * availability_effect_hutan_primer_sekunder()
        * hutan_primer_sekunder()
    )


@component.add(
    name='"Hutan Tanaman to Hutan Primer & Sekunder"',
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hutan_tanaman_to_hutan_primer_sekunder_share": 1,
        "availability_effect_hutan_tanaman": 1,
        "hutan_tanaman": 1,
    },
)
def hutan_tanaman_to_hutan_primer_sekunder():
    return (
        hutan_tanaman_to_hutan_primer_sekunder_share()
        * availability_effect_hutan_tanaman()
        * hutan_tanaman()
    )


@component.add(
    name='"Hutan Primer & Hutan Sekunderke Pertambangan"',
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hutan_primer_sekunder_ke_pertambangan_share": 1,
        "availability_effect_hutan_primer_sekunder": 1,
        "hutan_primer_sekunder": 1,
    },
)
def hutan_primer_hutan_sekunderke_pertambangan():
    return (
        hutan_primer_sekunder_ke_pertambangan_share()
        * availability_effect_hutan_primer_sekunder()
        * hutan_primer_sekunder()
    )


@component.add(
    name='"Hutan Primer & Hutan Sekunder ke Rawa & Badan Air"',
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hutan_primer_sekunder_ke_rawa_badan_air_share": 1,
        "availability_effect_hutan_primer_sekunder": 1,
        "hutan_primer_sekunder": 1,
    },
)
def hutan_primer_hutan_sekunder_ke_rawa_badan_air():
    return (
        hutan_primer_sekunder_ke_rawa_badan_air_share()
        * availability_effect_hutan_primer_sekunder()
        * hutan_primer_sekunder()
    )


@component.add(
    name='"Hutan Primer & Hutan Sekunder to Pertanian"',
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hutan_primer_sekunder_to_pertanian_share": 1,
        "availability_effect_hutan_primer_sekunder": 1,
        "hutan_primer_sekunder": 1,
    },
)
def hutan_primer_hutan_sekunder_to_pertanian():
    return (
        hutan_primer_sekunder_to_pertanian_share()
        * availability_effect_hutan_primer_sekunder()
        * hutan_primer_sekunder()
    )


@component.add(
    name='"Rawa & Badan Air Init"',
    units="Ha",
    comp_type="Stateful",
    comp_subtype="Initial",
    depends_on={"_initial_rawa_badan_air_init": 1},
    other_deps={
        "_initial_rawa_badan_air_init": {
            "initial": {"rawa_badan_air_hist": 1},
            "step": {},
        }
    },
)
def rawa_badan_air_init():
    return _initial_rawa_badan_air_init()


_initial_rawa_badan_air_init = Initial(
    lambda: rawa_badan_air_hist(), "_initial_rawa_badan_air_init"
)


@component.add(
    name="Total Lahan",
    units="Ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hutan_primer_sekunder": 1,
        "lahan_lainnya": 1,
        "lahan_terbangun": 1,
        "belukar_padang_rumput": 1,
        "perkebunan": 1,
        "pertambangan": 1,
        "hutan_mangrove": 1,
        "hutan_tanaman": 1,
        "pertanian": 1,
        "rawa_badan_air": 1,
    },
)
def total_lahan():
    return (
        hutan_primer_sekunder()
        + lahan_lainnya()
        + lahan_terbangun()
        + belukar_padang_rumput()
        + perkebunan()
        + pertambangan()
        + hutan_mangrove()
        + hutan_tanaman()
        + pertanian()
        + rawa_badan_air()
    )


@component.add(
    name="Hutan Tanaman",
    units="Ha",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_hutan_tanaman": 1},
    other_deps={
        "_integ_hutan_tanaman": {
            "initial": {"hutan_tanaman_init": 1},
            "step": {
                "hutan_primer_hutan_sekunder_to_hutan_tanaman": 1,
                "rawa_badan_air_ke_hutan_tanaman": 1,
                "lahan_lainnya_ke_hutan_tanaman": 1,
                "lahan_terbangun_to_hutan_tanaman": 1,
                "belukar_padang_rumput_to_hutan_tanaman": 1,
                "perkebunan_to_hutan_tanaman": 1,
                "pertambangan_ke_hutan_tanaman": 1,
                "hutan_mangrove_to_hutan_tanaman": 1,
                "pertanian_to_hutan_tanaman": 1,
                "hutan_tanaman_ke_rawa_badan_air": 1,
                "hutan_tanaman_ke_lahan_lainnya": 1,
                "hutan_tanaman_ke_pertambangan": 1,
                "hutan_tanaman_to_hutan_primer_sekunder": 1,
                "hutan_tanaman_to_lahan_terbangun": 1,
                "hutan_tanaman_to_belukar_padang_rumput": 1,
                "hutan_tanaman_to_perkebunan": 1,
                "hutan_tanaman_to_hutan_mangrove": 1,
                "hutan_tanaman_to_pertanian": 1,
            },
        }
    },
)
def hutan_tanaman():
    return _integ_hutan_tanaman()


_integ_hutan_tanaman = Integ(
    lambda: hutan_primer_hutan_sekunder_to_hutan_tanaman()
    + rawa_badan_air_ke_hutan_tanaman()
    + lahan_lainnya_ke_hutan_tanaman()
    + lahan_terbangun_to_hutan_tanaman()
    + belukar_padang_rumput_to_hutan_tanaman()
    + perkebunan_to_hutan_tanaman()
    + pertambangan_ke_hutan_tanaman()
    + hutan_mangrove_to_hutan_tanaman()
    + pertanian_to_hutan_tanaman()
    - hutan_tanaman_ke_rawa_badan_air()
    - hutan_tanaman_ke_lahan_lainnya()
    - hutan_tanaman_ke_pertambangan()
    - hutan_tanaman_to_hutan_primer_sekunder()
    - hutan_tanaman_to_lahan_terbangun()
    - hutan_tanaman_to_belukar_padang_rumput()
    - hutan_tanaman_to_perkebunan()
    - hutan_tanaman_to_hutan_mangrove()
    - hutan_tanaman_to_pertanian(),
    lambda: hutan_tanaman_init(),
    "_integ_hutan_tanaman",
)


@component.add(
    name='"Hutan Primer & Sekunder"',
    units="Ha",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_hutan_primer_sekunder": 1},
    other_deps={
        "_integ_hutan_primer_sekunder": {
            "initial": {"hutan_primer_sekunder_init": 1},
            "step": {
                "rawa_badan_air_ke_hutan_primer_sekunder": 1,
                "lahan_lainnya_ke_hutan_primer_sekunder": 1,
                "lahan_terbangun_to_hutan_primer_sekunder": 1,
                "belukar_padang_rumput_to_hutan_primer_sekunder": 1,
                "perkebunan_to_hutan_primer_sekunder": 1,
                "pertambangan_ke_hutan_primer_sekunder": 1,
                "hutan_mangrove_to_hutan_primer_sekunder": 1,
                "hutan_tanaman_to_hutan_primer_sekunder": 1,
                "pertanian_to_hutan_primer_sekunder": 1,
                "hutan_primer_hutan_sekunder_ke_rawa_badan_air": 1,
                "hutan_primer_hutan_sekunderke_pertambangan": 1,
                "hutan_primer_hutan_sekunder_ke_lahan_lainnya": 1,
                "hutan_primer_hutan_sekunder_to_lahan_terbangun": 1,
                "hutan_primer_hutan_sekunder_to_belukar_padang_rumput": 1,
                "hutan_primer_hutan_sekunder_to_perkebunan": 1,
                "hutan_primer_hutan_sekunder_to_hutan_mangrove": 1,
                "hutan_primer_hutan_sekunder_to_hutan_tanaman": 1,
                "hutan_primer_hutan_sekunder_to_pertanian": 1,
            },
        }
    },
)
def hutan_primer_sekunder():
    return _integ_hutan_primer_sekunder()


_integ_hutan_primer_sekunder = Integ(
    lambda: rawa_badan_air_ke_hutan_primer_sekunder()
    + lahan_lainnya_ke_hutan_primer_sekunder()
    + lahan_terbangun_to_hutan_primer_sekunder()
    + belukar_padang_rumput_to_hutan_primer_sekunder()
    + perkebunan_to_hutan_primer_sekunder()
    + pertambangan_ke_hutan_primer_sekunder()
    + hutan_mangrove_to_hutan_primer_sekunder()
    + hutan_tanaman_to_hutan_primer_sekunder()
    + pertanian_to_hutan_primer_sekunder()
    - hutan_primer_hutan_sekunder_ke_rawa_badan_air()
    - hutan_primer_hutan_sekunderke_pertambangan()
    - hutan_primer_hutan_sekunder_ke_lahan_lainnya()
    - hutan_primer_hutan_sekunder_to_lahan_terbangun()
    - hutan_primer_hutan_sekunder_to_belukar_padang_rumput()
    - hutan_primer_hutan_sekunder_to_perkebunan()
    - hutan_primer_hutan_sekunder_to_hutan_mangrove()
    - hutan_primer_hutan_sekunder_to_hutan_tanaman()
    - hutan_primer_hutan_sekunder_to_pertanian(),
    lambda: hutan_primer_sekunder_init(),
    "_integ_hutan_primer_sekunder",
)


@component.add(
    name="Belukar Padang Rumput Minimum",
    units="Ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "belukar_padang_rumput_init": 1,
        "minimum_fraction_belukar_padang_rumput": 1,
    },
)
def belukar_padang_rumput_minimum():
    return belukar_padang_rumput_init() * minimum_fraction_belukar_padang_rumput()


@component.add(
    name='"Availability Effect Hutan Primer & Sekunder"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"hutan_primer_sekunder_ratio": 1},
)
def availability_effect_hutan_primer_sekunder():
    return np.interp(
        hutan_primer_sekunder_ratio(),
        [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0],
        [0.0, 0.0, 0.14, 0.255, 0.426, 0.574, 0.71, 0.83, 0.91, 0.97, 1.0],
    )


@component.add(
    name='"Availability Effect Rawa & Badan Air"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"rawa_badan_air_ratio": 1},
)
def availability_effect_rawa_badan_air():
    return np.interp(
        rawa_badan_air_ratio(),
        [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0],
        [0.0, 0.0, 0.14, 0.255, 0.426, 0.574, 0.71, 0.83, 0.91, 0.97, 1.0],
    )


@component.add(
    name="Availability Effect Lahan Lainnya",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"lahan_lainnya_ratio": 1},
)
def availability_effect_lahan_lainnya():
    return np.interp(
        lahan_lainnya_ratio(),
        [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0],
        [0.0, 0.0, 0.14, 0.255, 0.426, 0.574, 0.71, 0.83, 0.91, 0.97, 1.0],
    )


@component.add(
    name="Availability Effect Lahan Terbangun",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"lahan_terbangun_ratio": 1},
)
def availability_effect_lahan_terbangun():
    return np.interp(
        lahan_terbangun_ratio(),
        [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0],
        [0.0, 0.0, 0.14, 0.255, 0.426, 0.574, 0.71, 0.83, 0.91, 0.97, 1.0],
    )


@component.add(
    name="Availability Effect Belukar Padang Rumput",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"belukar_padang_rumput_ratio": 1},
)
def availability_effect_belukar_padang_rumput():
    return np.interp(
        belukar_padang_rumput_ratio(),
        [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0],
        [0.0, 0.0, 0.14, 0.255, 0.426, 0.574, 0.71, 0.83, 0.91, 0.97, 1.0],
    )


@component.add(
    name="Availability Effect Perkebunan",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"perkebunan_ratio": 1},
)
def availability_effect_perkebunan():
    return np.interp(
        perkebunan_ratio(),
        [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0],
        [0.0, 0.0, 0.14, 0.255, 0.426, 0.574, 0.71, 0.83, 0.91, 0.97, 1.0],
    )


@component.add(
    name="Availability Effect Pertambangan",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"pertambangan_ratio": 1},
)
def availability_effect_pertambangan():
    return np.interp(
        pertambangan_ratio(),
        [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0],
        [0.0, 0.0, 0.14, 0.255, 0.426, 0.574, 0.71, 0.83, 0.91, 0.97, 1.0],
    )


@component.add(
    name="Availability Effect Hutan Mangrove",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"mangrove_ratio": 1},
)
def availability_effect_hutan_mangrove():
    return np.interp(
        mangrove_ratio(),
        [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0],
        [0.0, 0.0, 0.14, 0.255, 0.426, 0.574, 0.71, 0.83, 0.91, 0.97, 1.0],
    )


@component.add(
    name="Availability Effect Hutan Tanaman",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"hutan_tanaman_ratio": 1},
)
def availability_effect_hutan_tanaman():
    return np.interp(
        hutan_tanaman_ratio(),
        [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0],
        [0.0, 0.0, 0.14, 0.255, 0.426, 0.574, 0.71, 0.83, 0.91, 0.97, 1.0],
    )


@component.add(
    name="Availability Effect Pertanian",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"pertanian_ratio": 1},
)
def availability_effect_pertanian():
    return np.interp(
        pertanian_ratio(),
        [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0],
        [0.0, 0.0, 0.14, 0.255, 0.426, 0.574, 0.71, 0.83, 0.91, 0.97, 1.0],
    )


@component.add(
    name="Pertambangan Minimum",
    units="Ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pertambangan_init": 1, "minimum_fraction_pertambangan": 1},
)
def pertambangan_minimum():
    return pertambangan_init() * minimum_fraction_pertambangan()


@component.add(
    name="Hutan Mangrove",
    units="Ha",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_hutan_mangrove": 1},
    other_deps={
        "_integ_hutan_mangrove": {
            "initial": {"hutan_mangrove_init": 1},
            "step": {
                "hutan_primer_hutan_sekunder_to_hutan_mangrove": 1,
                "rawa_badan_air_ke_hutan_mangrove": 1,
                "lahan_lainnya_ke_hutan_mangrove": 1,
                "lahan_terbangun_to_hutan_mangrove": 1,
                "belukar_padang_rumput_to_hutan_mangrove": 1,
                "perkebunan_to_hutan_mangrove": 1,
                "pertambangan_ke_hutan_mangrove": 1,
                "hutan_tanaman_to_hutan_mangrove": 1,
                "pertanian_to_hutan_mangrove": 1,
                "hutan_mangrove_ke_rawa_badan_air": 1,
                "hutan_mangrove_ke_lahan_lainnya": 1,
                "hutan_mangrove_ke_pertambangan": 1,
                "hutan_mangrove_to_hutan_primer_sekunder": 1,
                "hutan_mangrove_to_lahan_terbangun": 1,
                "hutan_mangrove_to_belukar_padang_rumput": 1,
                "hutan_mangrove_to_perkebunan": 1,
                "hutan_mangrove_to_hutan_tanaman": 1,
                "hutan_mangrove_to_pertanian": 1,
            },
        }
    },
)
def hutan_mangrove():
    return _integ_hutan_mangrove()


_integ_hutan_mangrove = Integ(
    lambda: hutan_primer_hutan_sekunder_to_hutan_mangrove()
    + rawa_badan_air_ke_hutan_mangrove()
    + lahan_lainnya_ke_hutan_mangrove()
    + lahan_terbangun_to_hutan_mangrove()
    + belukar_padang_rumput_to_hutan_mangrove()
    + perkebunan_to_hutan_mangrove()
    + pertambangan_ke_hutan_mangrove()
    + hutan_tanaman_to_hutan_mangrove()
    + pertanian_to_hutan_mangrove()
    - hutan_mangrove_ke_rawa_badan_air()
    - hutan_mangrove_ke_lahan_lainnya()
    - hutan_mangrove_ke_pertambangan()
    - hutan_mangrove_to_hutan_primer_sekunder()
    - hutan_mangrove_to_lahan_terbangun()
    - hutan_mangrove_to_belukar_padang_rumput()
    - hutan_mangrove_to_perkebunan()
    - hutan_mangrove_to_hutan_tanaman()
    - hutan_mangrove_to_pertanian(),
    lambda: hutan_mangrove_init(),
    "_integ_hutan_mangrove",
)


@component.add(
    name="Perkebunan",
    units="Ha",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_perkebunan": 1},
    other_deps={
        "_integ_perkebunan": {
            "initial": {"perkebunan_init": 1},
            "step": {
                "hutan_primer_hutan_sekunder_to_perkebunan": 1,
                "rawa_badan_air_ke_perkebunan": 1,
                "lahan_lainnya_ke_perkebunan": 1,
                "lahan_terbangun_to_perkebunan": 1,
                "belukar_padang_rumput_to_perkebunan": 1,
                "pertambangan_ke_perkebunan": 1,
                "hutan_mangrove_to_perkebunan": 1,
                "hutan_tanaman_to_perkebunan": 1,
                "pertanian_to_perkebunan": 1,
                "perkebunan_ke_rawa_badan_air": 1,
                "perkebunan_ke_lahan_lainnya": 1,
                "perkebunan_ke_pertambangan": 1,
                "perkebunan_to_hutan_primer_sekunder": 1,
                "perkebunan_to_lahan_terbangun": 1,
                "perkebunan_to_belukar_padang_rumput": 1,
                "perkebunan_to_hutan_mangrove": 1,
                "perkebunan_to_hutan_tanaman": 1,
                "perkebunan_to_pertanian": 1,
            },
        }
    },
)
def perkebunan():
    return _integ_perkebunan()


_integ_perkebunan = Integ(
    lambda: hutan_primer_hutan_sekunder_to_perkebunan()
    + rawa_badan_air_ke_perkebunan()
    + lahan_lainnya_ke_perkebunan()
    + lahan_terbangun_to_perkebunan()
    + belukar_padang_rumput_to_perkebunan()
    + pertambangan_ke_perkebunan()
    + hutan_mangrove_to_perkebunan()
    + hutan_tanaman_to_perkebunan()
    + pertanian_to_perkebunan()
    - perkebunan_ke_rawa_badan_air()
    - perkebunan_ke_lahan_lainnya()
    - perkebunan_ke_pertambangan()
    - perkebunan_to_hutan_primer_sekunder()
    - perkebunan_to_lahan_terbangun()
    - perkebunan_to_belukar_padang_rumput()
    - perkebunan_to_hutan_mangrove()
    - perkebunan_to_hutan_tanaman()
    - perkebunan_to_pertanian(),
    lambda: perkebunan_init(),
    "_integ_perkebunan",
)


@component.add(
    name="Lahan Lainnya",
    units="Ha",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_lahan_lainnya": 1},
    other_deps={
        "_integ_lahan_lainnya": {
            "initial": {"lahan_lainnya_init": 1},
            "step": {
                "hutan_primer_hutan_sekunder_ke_lahan_lainnya": 1,
                "rawa_badan_air_ke_lahan_lainnya": 1,
                "lahan_terbangun_ke_lahan_lainnya": 1,
                "belukar_padang_rumput_ke_lahan_lainnya": 1,
                "perkebunan_ke_lahan_lainnya": 1,
                "pertambangan_ke_lahan_lainnya": 1,
                "hutan_mangrove_ke_lahan_lainnya": 1,
                "hutan_tanaman_ke_lahan_lainnya": 1,
                "pertanian_ke_lahan_lainnya": 1,
                "lahan_lainnya_ke_rawa_badan_air": 1,
                "lahan_lainnya_ke_hutan_primer_sekunder": 1,
                "lahan_lainnya_ke_lahan_terbangun": 1,
                "lahan_lainnya_ke_belukar_padang_rumput": 1,
                "lahan_lainnya_ke_perkebunan": 1,
                "lahan_lainnya_ke_pertambangan": 1,
                "lahan_lainnya_ke_hutan_mangrove": 1,
                "lahan_lainnya_ke_hutan_tanaman": 1,
                "lahan_lainnya_ke_pertanian": 1,
            },
        }
    },
)
def lahan_lainnya():
    return _integ_lahan_lainnya()


_integ_lahan_lainnya = Integ(
    lambda: hutan_primer_hutan_sekunder_ke_lahan_lainnya()
    + rawa_badan_air_ke_lahan_lainnya()
    + lahan_terbangun_ke_lahan_lainnya()
    + belukar_padang_rumput_ke_lahan_lainnya()
    + perkebunan_ke_lahan_lainnya()
    + pertambangan_ke_lahan_lainnya()
    + hutan_mangrove_ke_lahan_lainnya()
    + hutan_tanaman_ke_lahan_lainnya()
    + pertanian_ke_lahan_lainnya()
    - lahan_lainnya_ke_rawa_badan_air()
    - lahan_lainnya_ke_hutan_primer_sekunder()
    - lahan_lainnya_ke_lahan_terbangun()
    - lahan_lainnya_ke_belukar_padang_rumput()
    - lahan_lainnya_ke_perkebunan()
    - lahan_lainnya_ke_pertambangan()
    - lahan_lainnya_ke_hutan_mangrove()
    - lahan_lainnya_ke_hutan_tanaman()
    - lahan_lainnya_ke_pertanian(),
    lambda: lahan_lainnya_init(),
    "_integ_lahan_lainnya",
)


@component.add(
    name="Perkebunan init",
    units="Ha",
    comp_type="Stateful",
    comp_subtype="Initial",
    depends_on={"_initial_perkebunan_init": 1},
    other_deps={
        "_initial_perkebunan_init": {"initial": {"perkebunan_hist": 1}, "step": {}}
    },
)
def perkebunan_init():
    return _initial_perkebunan_init()


_initial_perkebunan_init = Initial(
    lambda: perkebunan_hist(), "_initial_perkebunan_init"
)


@component.add(
    name="Lahan Lainnya Init",
    units="Ha",
    comp_type="Stateful",
    comp_subtype="Initial",
    depends_on={"_initial_lahan_lainnya_init": 1},
    other_deps={
        "_initial_lahan_lainnya_init": {
            "initial": {"lahan_lainnya_hist": 1},
            "step": {},
        }
    },
)
def lahan_lainnya_init():
    return _initial_lahan_lainnya_init()


_initial_lahan_lainnya_init = Initial(
    lambda: lahan_lainnya_hist(), "_initial_lahan_lainnya_init"
)


@component.add(
    name="Perkebunan Minimum",
    units="Ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"perkebunan_init": 1, "minimum_fraction_perkebunan": 1},
)
def perkebunan_minimum():
    return perkebunan_init() * minimum_fraction_perkebunan()


@component.add(
    name="Perkebunan Ratio",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"perkebunan": 1, "perkebunan_minimum": 1},
)
def perkebunan_ratio():
    return perkebunan() / perkebunan_minimum()


@component.add(
    name="Hutan Tanaman init",
    units="Ha",
    comp_type="Stateful",
    comp_subtype="Initial",
    depends_on={"_initial_hutan_tanaman_init": 1},
    other_deps={
        "_initial_hutan_tanaman_init": {
            "initial": {"hutan_tanaman_hist": 1},
            "step": {},
        }
    },
)
def hutan_tanaman_init():
    return _initial_hutan_tanaman_init()


_initial_hutan_tanaman_init = Initial(
    lambda: hutan_tanaman_hist(), "_initial_hutan_tanaman_init"
)


@component.add(
    name='"Hutan Primer & Sekunder init"',
    units="Ha",
    comp_type="Stateful",
    comp_subtype="Initial",
    depends_on={"_initial_hutan_primer_sekunder_init": 1},
    other_deps={
        "_initial_hutan_primer_sekunder_init": {
            "initial": {"hutan_primer_sekunder_hist": 1},
            "step": {},
        }
    },
)
def hutan_primer_sekunder_init():
    return _initial_hutan_primer_sekunder_init()


_initial_hutan_primer_sekunder_init = Initial(
    lambda: hutan_primer_sekunder_hist(), "_initial_hutan_primer_sekunder_init"
)


@component.add(
    name="Pertambangan Init",
    units="Ha",
    comp_type="Stateful",
    comp_subtype="Initial",
    depends_on={"_initial_pertambangan_init": 1},
    other_deps={
        "_initial_pertambangan_init": {"initial": {"pertambangan_hist": 1}, "step": {}}
    },
)
def pertambangan_init():
    return _initial_pertambangan_init()


_initial_pertambangan_init = Initial(
    lambda: pertambangan_hist(), "_initial_pertambangan_init"
)


@component.add(
    name='"Hutan Primer & Sekunder Minimum"',
    units="Ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hutan_primer_sekunder_init": 1,
        "minimum_fraction_hutan_primer_sekunder": 1,
    },
)
def hutan_primer_sekunder_minimum():
    return hutan_primer_sekunder_init() * minimum_fraction_hutan_primer_sekunder()


@component.add(
    name='"Hutan Primer & Sekunder Ratio"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hutan_primer_sekunder": 1, "hutan_primer_sekunder_minimum": 1},
)
def hutan_primer_sekunder_ratio():
    return hutan_primer_sekunder() / hutan_primer_sekunder_minimum()


@component.add(
    name="Lahan Terbangun Minimum",
    units="Ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"lahan_terbangun_init": 1, "minimum_fraction_lahan_terbangun": 1},
)
def lahan_terbangun_minimum():
    return lahan_terbangun_init() * minimum_fraction_lahan_terbangun()


@component.add(
    name="Pertambangan Ratio",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pertambangan": 1, "pertambangan_minimum": 1},
)
def pertambangan_ratio():
    return pertambangan() / pertambangan_minimum()


@component.add(
    name="Hutan Mangrove init",
    units="Ha",
    comp_type="Stateful",
    comp_subtype="Initial",
    depends_on={"_initial_hutan_mangrove_init": 1},
    other_deps={
        "_initial_hutan_mangrove_init": {
            "initial": {"hutan_mangrove_hist": 1},
            "step": {},
        }
    },
)
def hutan_mangrove_init():
    return _initial_hutan_mangrove_init()


_initial_hutan_mangrove_init = Initial(
    lambda: hutan_mangrove_hist(), "_initial_hutan_mangrove_init"
)


@component.add(
    name="Time Index",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "time_unit": 1},
)
def time_index():
    return time() / time_unit()


@component.add(
    name='"Rawa & Badan Air Minimum"',
    units="Ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"rawa_badan_air_init": 1, "minimum_fraction_rawa_badan_air": 1},
)
def rawa_badan_air_minimum():
    return rawa_badan_air_init() * minimum_fraction_rawa_badan_air()


@component.add(
    name='"Rawa & Badan Air Ratio"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"rawa_badan_air": 1, "rawa_badan_air_minimum": 1},
)
def rawa_badan_air_ratio():
    return rawa_badan_air() / rawa_badan_air_minimum()


@component.add(
    name='"Rawa & Badan Air"',
    units="Ha",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_rawa_badan_air": 1},
    other_deps={
        "_integ_rawa_badan_air": {
            "initial": {"rawa_badan_air_init": 1},
            "step": {
                "hutan_primer_hutan_sekunder_ke_rawa_badan_air": 1,
                "lahan_lainnya_ke_rawa_badan_air": 1,
                "lahan_terbangun_ke_rawa_badan_air": 1,
                "belukar_padang_rumput_ke_rawa_badan_air": 1,
                "perkebunan_ke_rawa_badan_air": 1,
                "pertambangan_ke_rawa_badan_air": 1,
                "hutan_mangrove_ke_rawa_badan_air": 1,
                "hutan_tanaman_ke_rawa_badan_air": 1,
                "pertanian_ke_rawa_badan_air": 1,
                "rawa_badan_air_ke_hutan_primer_sekunder": 1,
                "rawa_badan_air_ke_lahan_terbangun": 1,
                "rawa_badan_air_ke_belukar_padang_rumput": 1,
                "rawa_badan_air_ke_perkebunan": 1,
                "rawa_badan_air_ke_pertambangan": 1,
                "rawa_badan_air_ke_hutan_mangrove": 1,
                "rawa_badan_air_ke_hutan_tanaman": 1,
                "rawa_badan_air_ke_pertanian": 1,
                "rawa_badan_air_ke_lahan_lainnya": 1,
            },
        }
    },
)
def rawa_badan_air():
    return _integ_rawa_badan_air()


_integ_rawa_badan_air = Integ(
    lambda: hutan_primer_hutan_sekunder_ke_rawa_badan_air()
    + lahan_lainnya_ke_rawa_badan_air()
    + lahan_terbangun_ke_rawa_badan_air()
    + belukar_padang_rumput_ke_rawa_badan_air()
    + perkebunan_ke_rawa_badan_air()
    + pertambangan_ke_rawa_badan_air()
    + hutan_mangrove_ke_rawa_badan_air()
    + hutan_tanaman_ke_rawa_badan_air()
    + pertanian_ke_rawa_badan_air()
    - rawa_badan_air_ke_hutan_primer_sekunder()
    - rawa_badan_air_ke_lahan_terbangun()
    - rawa_badan_air_ke_belukar_padang_rumput()
    - rawa_badan_air_ke_perkebunan()
    - rawa_badan_air_ke_pertambangan()
    - rawa_badan_air_ke_hutan_mangrove()
    - rawa_badan_air_ke_hutan_tanaman()
    - rawa_badan_air_ke_pertanian()
    - rawa_badan_air_ke_lahan_lainnya(),
    lambda: rawa_badan_air_init(),
    "_integ_rawa_badan_air",
)


@component.add(
    name="Minimum Fraction Belukar Padang Rumput",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def minimum_fraction_belukar_padang_rumput():
    return np.interp(
        time_index(),
        [
            2000.0,
            2001.0,
            2002.0,
            2003.0,
            2004.0,
            2005.0,
            2006.0,
            2007.0,
            2008.0,
            2009.0,
            2010.0,
            2011.0,
            2012.0,
            2013.0,
            2014.0,
            2015.0,
            2016.0,
            2017.0,
        ],
        [
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
        ],
    )


@component.add(
    name="Minimum Fraction Pertambangan",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def minimum_fraction_pertambangan():
    return np.interp(
        time_index(),
        [
            2000.0,
            2001.0,
            2002.0,
            2003.0,
            2004.0,
            2005.0,
            2006.0,
            2007.0,
            2008.0,
            2009.0,
            2010.0,
            2011.0,
            2012.0,
            2013.0,
            2014.0,
            2015.0,
            2016.0,
            2017.0,
        ],
        [
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
        ],
    )


@component.add(
    name="Minimum Fraction Hutan Tanaman",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def minimum_fraction_hutan_tanaman():
    return np.interp(
        time_index(),
        [
            2000.0,
            2001.0,
            2002.0,
            2003.0,
            2004.0,
            2005.0,
            2006.0,
            2007.0,
            2008.0,
            2009.0,
            2010.0,
            2011.0,
            2012.0,
            2013.0,
            2014.0,
            2015.0,
            2016.0,
            2017.0,
        ],
        [
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
        ],
    )


@component.add(
    name="Minimum Fraction Pertanian",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def minimum_fraction_pertanian():
    return np.interp(
        time_index(),
        [
            2000.0,
            2001.0,
            2002.0,
            2003.0,
            2004.0,
            2005.0,
            2006.0,
            2007.0,
            2008.0,
            2009.0,
            2010.0,
            2011.0,
            2012.0,
            2013.0,
            2014.0,
            2015.0,
            2016.0,
            2017.0,
        ],
        [
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
        ],
    )


@component.add(
    name="Belukar Padang Rumput",
    units="Ha",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_belukar_padang_rumput": 1},
    other_deps={
        "_integ_belukar_padang_rumput": {
            "initial": {"belukar_padang_rumput_init": 1},
            "step": {
                "hutan_primer_hutan_sekunder_to_belukar_padang_rumput": 1,
                "rawa_badan_air_ke_belukar_padang_rumput": 1,
                "lahan_lainnya_ke_belukar_padang_rumput": 1,
                "lahan_terbangun_to_belukar_padang_rumput": 1,
                "perkebunan_to_belukar_padang_rumput": 1,
                "pertambangan_ke_belukar_padang_rumput": 1,
                "hutan_mangrove_to_belukar_padang_rumput": 1,
                "hutan_tanaman_to_belukar_padang_rumput": 1,
                "pertanian_to_belukar_padang_rumput": 1,
                "belukar_padang_rumput_ke_rawa_badan_air": 1,
                "belukar_padang_rumput_ke_lahan_lainnya": 1,
                "belukar_padang_rumput_ke_pertambangan": 1,
                "belukar_padang_rumput_to_hutan_primer_sekunder": 1,
                "belukar_padang_rumput_to_lahan_terbangun": 1,
                "belukar_padang_rumput_to_perkebunan": 1,
                "belukar_padang_rumput_to_hutan_mangrove": 1,
                "belukar_padang_rumput_to_hutan_tanaman": 1,
                "belukar_padang_rumput_to_pertanian": 1,
            },
        }
    },
)
def belukar_padang_rumput():
    return _integ_belukar_padang_rumput()


_integ_belukar_padang_rumput = Integ(
    lambda: hutan_primer_hutan_sekunder_to_belukar_padang_rumput()
    + rawa_badan_air_ke_belukar_padang_rumput()
    + lahan_lainnya_ke_belukar_padang_rumput()
    + lahan_terbangun_to_belukar_padang_rumput()
    + perkebunan_to_belukar_padang_rumput()
    + pertambangan_ke_belukar_padang_rumput()
    + hutan_mangrove_to_belukar_padang_rumput()
    + hutan_tanaman_to_belukar_padang_rumput()
    + pertanian_to_belukar_padang_rumput()
    - belukar_padang_rumput_ke_rawa_badan_air()
    - belukar_padang_rumput_ke_lahan_lainnya()
    - belukar_padang_rumput_ke_pertambangan()
    - belukar_padang_rumput_to_hutan_primer_sekunder()
    - belukar_padang_rumput_to_lahan_terbangun()
    - belukar_padang_rumput_to_perkebunan()
    - belukar_padang_rumput_to_hutan_mangrove()
    - belukar_padang_rumput_to_hutan_tanaman()
    - belukar_padang_rumput_to_pertanian(),
    lambda: belukar_padang_rumput_init(),
    "_integ_belukar_padang_rumput",
)


@component.add(
    name="Belukar Padang Rumput init",
    units="Ha",
    comp_type="Stateful",
    comp_subtype="Initial",
    depends_on={"_initial_belukar_padang_rumput_init": 1},
    other_deps={
        "_initial_belukar_padang_rumput_init": {
            "initial": {"belukar_padang_rumput_hist": 1},
            "step": {},
        }
    },
)
def belukar_padang_rumput_init():
    return _initial_belukar_padang_rumput_init()


_initial_belukar_padang_rumput_init = Initial(
    lambda: belukar_padang_rumput_hist(), "_initial_belukar_padang_rumput_init"
)


@component.add(
    name="Lahan Lainnya Minimum",
    units="Ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"lahan_lainnya_init": 1, "minimum_fraction_lahan_lainnya": 1},
)
def lahan_lainnya_minimum():
    return lahan_lainnya_init() * minimum_fraction_lahan_lainnya()


@component.add(
    name="Lahan Lainnya Ratio",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"lahan_lainnya": 1, "lahan_lainnya_minimum": 1},
)
def lahan_lainnya_ratio():
    return lahan_lainnya() / lahan_lainnya_minimum()


@component.add(
    name="Pertambangan",
    units="Ha",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_pertambangan": 1},
    other_deps={
        "_integ_pertambangan": {
            "initial": {"pertambangan_init": 1},
            "step": {
                "hutan_primer_hutan_sekunderke_pertambangan": 1,
                "rawa_badan_air_ke_pertambangan": 1,
                "lahan_lainnya_ke_pertambangan": 1,
                "lahan_terbangun_ke_pertambangan": 1,
                "belukar_padang_rumput_ke_pertambangan": 1,
                "perkebunan_ke_pertambangan": 1,
                "hutan_mangrove_ke_pertambangan": 1,
                "hutan_tanaman_ke_pertambangan": 1,
                "pertanian_ke_pertambangan": 1,
                "pertambangan_ke_hutan_primer_sekunder": 1,
                "pertambangan_ke_rawa_badan_air": 1,
                "pertambangan_ke_lahan_lainnya": 1,
                "pertambangan_ke_lahan_terbangun": 1,
                "pertambangan_ke_belukar_padang_rumput": 1,
                "pertambangan_ke_perkebunan": 1,
                "pertambangan_ke_hutan_mangrove": 1,
                "pertambangan_ke_hutan_tanaman": 1,
                "pertambangan_ke_pertanian": 1,
            },
        }
    },
)
def pertambangan():
    return _integ_pertambangan()


_integ_pertambangan = Integ(
    lambda: hutan_primer_hutan_sekunderke_pertambangan()
    + rawa_badan_air_ke_pertambangan()
    + lahan_lainnya_ke_pertambangan()
    + lahan_terbangun_ke_pertambangan()
    + belukar_padang_rumput_ke_pertambangan()
    + perkebunan_ke_pertambangan()
    + hutan_mangrove_ke_pertambangan()
    + hutan_tanaman_ke_pertambangan()
    + pertanian_ke_pertambangan()
    - pertambangan_ke_hutan_primer_sekunder()
    - pertambangan_ke_rawa_badan_air()
    - pertambangan_ke_lahan_lainnya()
    - pertambangan_ke_lahan_terbangun()
    - pertambangan_ke_belukar_padang_rumput()
    - pertambangan_ke_perkebunan()
    - pertambangan_ke_hutan_mangrove()
    - pertambangan_ke_hutan_tanaman()
    - pertambangan_ke_pertanian(),
    lambda: pertambangan_init(),
    "_integ_pertambangan",
)


@component.add(
    name="Pertanian init",
    units="Ha",
    comp_type="Stateful",
    comp_subtype="Initial",
    depends_on={"_initial_pertanian_init": 1},
    other_deps={
        "_initial_pertanian_init": {"initial": {"pertanian_hist": 1}, "step": {}}
    },
)
def pertanian_init():
    """
    9.98742e+06
    """
    return _initial_pertanian_init()


_initial_pertanian_init = Initial(lambda: pertanian_hist(), "_initial_pertanian_init")


@component.add(
    name="Belukar Padang Rumput Ratio",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"belukar_padang_rumput": 1, "belukar_padang_rumput_minimum": 1},
)
def belukar_padang_rumput_ratio():
    return belukar_padang_rumput() / belukar_padang_rumput_minimum()


@component.add(
    name="Hutan Tanaman Minimum",
    units="Ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hutan_tanaman_init": 1, "minimum_fraction_hutan_tanaman": 1},
)
def hutan_tanaman_minimum():
    return hutan_tanaman_init() * minimum_fraction_hutan_tanaman()


@component.add(
    name="Hutan Tanaman Ratio",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hutan_tanaman": 1, "hutan_tanaman_minimum": 1},
)
def hutan_tanaman_ratio():
    return hutan_tanaman() / hutan_tanaman_minimum()


@component.add(
    name="kebutuhan air perkebunan SK 146",
    units="m*m*m/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "perkebunan": 1,
        "std_kebutuhan_air_per_perkebunan_sk_1462023_tahunan": 1,
    },
)
def kebutuhan_air_perkebunan_sk_146():
    return perkebunan() * std_kebutuhan_air_per_perkebunan_sk_1462023_tahunan()


@component.add(
    name='"Minimum Fraction Hutan Primer & Sekunder"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def minimum_fraction_hutan_primer_sekunder():
    return np.interp(
        time_index(),
        [
            2000.0,
            2001.0,
            2002.0,
            2003.0,
            2004.0,
            2005.0,
            2006.0,
            2007.0,
            2008.0,
            2009.0,
            2010.0,
            2011.0,
            2012.0,
            2013.0,
            2014.0,
            2015.0,
            2016.0,
            2017.0,
        ],
        [
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
        ],
    )


@component.add(
    name='"Minimum Fraction Rawa & Badan Air"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def minimum_fraction_rawa_badan_air():
    return np.interp(
        time_index(),
        [
            2000.0,
            2001.0,
            2002.0,
            2003.0,
            2004.0,
            2005.0,
            2006.0,
            2007.0,
            2008.0,
            2009.0,
            2010.0,
            2011.0,
            2012.0,
            2013.0,
            2014.0,
            2015.0,
            2016.0,
            2017.0,
        ],
        [
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
        ],
    )


@component.add(
    name="Pertanian",
    units="Ha",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_pertanian": 1},
    other_deps={
        "_integ_pertanian": {
            "initial": {"pertanian_init": 1},
            "step": {
                "hutan_primer_hutan_sekunder_to_pertanian": 1,
                "rawa_badan_air_ke_pertanian": 1,
                "lahan_lainnya_ke_pertanian": 1,
                "lahan_terbangun_to_pertanian": 1,
                "belukar_padang_rumput_to_pertanian": 1,
                "perkebunan_to_pertanian": 1,
                "pertambangan_ke_pertanian": 1,
                "hutan_mangrove_to_pertanian": 1,
                "hutan_tanaman_to_pertanian": 1,
                "pertanian_ke_rawa_badan_air": 1,
                "pertanian_ke_lahan_lainnya": 1,
                "pertanian_ke_pertambangan": 1,
                "pertanian_to_hutan_primer_sekunder": 1,
                "pertanian_to_lahan_terbangun": 1,
                "pertanian_to_belukar_padang_rumput": 1,
                "pertanian_to_perkebunan": 1,
                "pertanian_to_hutan_mangrove": 1,
                "pertanian_to_hutan_tanaman": 1,
            },
        }
    },
)
def pertanian():
    return _integ_pertanian()


_integ_pertanian = Integ(
    lambda: hutan_primer_hutan_sekunder_to_pertanian()
    + rawa_badan_air_ke_pertanian()
    + lahan_lainnya_ke_pertanian()
    + lahan_terbangun_to_pertanian()
    + belukar_padang_rumput_to_pertanian()
    + perkebunan_to_pertanian()
    + pertambangan_ke_pertanian()
    + hutan_mangrove_to_pertanian()
    + hutan_tanaman_to_pertanian()
    - pertanian_ke_rawa_badan_air()
    - pertanian_ke_lahan_lainnya()
    - pertanian_ke_pertambangan()
    - pertanian_to_hutan_primer_sekunder()
    - pertanian_to_lahan_terbangun()
    - pertanian_to_belukar_padang_rumput()
    - pertanian_to_perkebunan()
    - pertanian_to_hutan_mangrove()
    - pertanian_to_hutan_tanaman(),
    lambda: pertanian_init(),
    "_integ_pertanian",
)


@component.add(
    name="Minimum Fraction Perkebunan",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def minimum_fraction_perkebunan():
    return np.interp(
        time_index(),
        [
            2000.0,
            2001.0,
            2002.0,
            2003.0,
            2004.0,
            2005.0,
            2006.0,
            2007.0,
            2008.0,
            2009.0,
            2010.0,
            2011.0,
            2012.0,
            2013.0,
            2014.0,
            2015.0,
            2016.0,
            2017.0,
        ],
        [
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
        ],
    )


@component.add(
    name="Lahan Terbangun",
    units="Ha",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_lahan_terbangun": 1},
    other_deps={
        "_integ_lahan_terbangun": {
            "initial": {"lahan_terbangun_init": 1},
            "step": {
                "hutan_primer_hutan_sekunder_to_lahan_terbangun": 1,
                "rawa_badan_air_ke_lahan_terbangun": 1,
                "lahan_lainnya_ke_lahan_terbangun": 1,
                "belukar_padang_rumput_to_lahan_terbangun": 1,
                "perkebunan_to_lahan_terbangun": 1,
                "pertambangan_ke_lahan_terbangun": 1,
                "hutan_mangrove_to_lahan_terbangun": 1,
                "hutan_tanaman_to_lahan_terbangun": 1,
                "pertanian_to_lahan_terbangun": 1,
                "lahan_terbangun_ke_rawa_badan_air": 1,
                "lahan_terbangun_ke_lahan_lainnya": 1,
                "lahan_terbangun_ke_pertambangan": 1,
                "lahan_terbangun_to_hutan_primer_sekunder": 1,
                "lahan_terbangun_to_belukar_padang_rumput": 1,
                "lahan_terbangun_to_perkebunan": 1,
                "lahan_terbangun_to_hutan_mangrove": 1,
                "lahan_terbangun_to_hutan_tanaman": 1,
                "lahan_terbangun_to_pertanian": 1,
            },
        }
    },
)
def lahan_terbangun():
    return _integ_lahan_terbangun()


_integ_lahan_terbangun = Integ(
    lambda: hutan_primer_hutan_sekunder_to_lahan_terbangun()
    + rawa_badan_air_ke_lahan_terbangun()
    + lahan_lainnya_ke_lahan_terbangun()
    + belukar_padang_rumput_to_lahan_terbangun()
    + perkebunan_to_lahan_terbangun()
    + pertambangan_ke_lahan_terbangun()
    + hutan_mangrove_to_lahan_terbangun()
    + hutan_tanaman_to_lahan_terbangun()
    + pertanian_to_lahan_terbangun()
    - lahan_terbangun_ke_rawa_badan_air()
    - lahan_terbangun_ke_lahan_lainnya()
    - lahan_terbangun_ke_pertambangan()
    - lahan_terbangun_to_hutan_primer_sekunder()
    - lahan_terbangun_to_belukar_padang_rumput()
    - lahan_terbangun_to_perkebunan()
    - lahan_terbangun_to_hutan_mangrove()
    - lahan_terbangun_to_hutan_tanaman()
    - lahan_terbangun_to_pertanian(),
    lambda: lahan_terbangun_init(),
    "_integ_lahan_terbangun",
)


@component.add(
    name="Time Unit", units="tahun", comp_type="Constant", comp_subtype="Normal"
)
def time_unit():
    return 1


@component.add(
    name="Pertanian Minimum",
    units="Ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pertanian_init": 1, "minimum_fraction_pertanian": 1},
)
def pertanian_minimum():
    return pertanian_init() * minimum_fraction_pertanian()


@component.add(
    name="Minimum Fraction Lahan Terbangun",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def minimum_fraction_lahan_terbangun():
    return np.interp(
        time_index(),
        [
            2000.0,
            2001.0,
            2002.0,
            2003.0,
            2004.0,
            2005.0,
            2006.0,
            2007.0,
            2008.0,
            2009.0,
            2010.0,
            2011.0,
            2012.0,
            2013.0,
            2014.0,
            2015.0,
            2016.0,
            2017.0,
        ],
        [
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
        ],
    )


@component.add(
    name="Lahan Terbangun Ratio",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"lahan_terbangun": 1, "lahan_terbangun_minimum": 1},
)
def lahan_terbangun_ratio():
    return lahan_terbangun() / lahan_terbangun_minimum()


@component.add(
    name="Minimum Fraction Mangrove",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def minimum_fraction_mangrove():
    return np.interp(
        time_index(),
        [
            2000.0,
            2001.0,
            2002.0,
            2003.0,
            2004.0,
            2005.0,
            2006.0,
            2007.0,
            2008.0,
            2009.0,
            2010.0,
            2011.0,
            2012.0,
            2013.0,
            2014.0,
            2015.0,
            2016.0,
            2017.0,
        ],
        [
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
        ],
    )


@component.add(
    name="Mangrove Minimum",
    units="Ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hutan_mangrove_init": 1, "minimum_fraction_mangrove": 1},
)
def mangrove_minimum():
    return hutan_mangrove_init() * minimum_fraction_mangrove()


@component.add(
    name="Mangrove Ratio",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hutan_mangrove": 1, "mangrove_minimum": 1},
)
def mangrove_ratio():
    return hutan_mangrove() / mangrove_minimum()


@component.add(
    name="Pertanian Ratio",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pertanian": 1, "pertanian_minimum": 1},
)
def pertanian_ratio():
    return pertanian() / pertanian_minimum()


@component.add(
    name="Lahan Terbangun init",
    units="Ha",
    comp_type="Stateful",
    comp_subtype="Initial",
    depends_on={"_initial_lahan_terbangun_init": 1},
    other_deps={
        "_initial_lahan_terbangun_init": {
            "initial": {"lahan_terbangun_hist": 1},
            "step": {},
        }
    },
)
def lahan_terbangun_init():
    """
    6.88015e+06
    """
    return _initial_lahan_terbangun_init()


_initial_lahan_terbangun_init = Initial(
    lambda: lahan_terbangun_hist(), "_initial_lahan_terbangun_init"
)


@component.add(
    name="Minimum Fraction Lahan Lainnya",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def minimum_fraction_lahan_lainnya():
    return np.interp(
        time_index(),
        [
            2000.0,
            2001.0,
            2002.0,
            2003.0,
            2004.0,
            2005.0,
            2006.0,
            2007.0,
            2008.0,
            2009.0,
            2010.0,
            2011.0,
            2012.0,
            2013.0,
            2014.0,
            2015.0,
            2016.0,
            2017.0,
        ],
        [
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
            0.1,
        ],
    )


@component.add(
    name="IKU Bali",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_iku_bali": 1},
    other_deps={"_integ_iku_bali": {"initial": {}, "step": {"perubahan_iku_bali": 1}}},
)
def iku_bali():
    """
    Interpolasi ke 2010
    """
    return _integ_iku_bali()


_integ_iku_bali = Integ(lambda: perubahan_iku_bali(), lambda: 94.7, "_integ_iku_bali")


@component.add(
    name="IKU Bali Historis",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def iku_bali_historis():
    return np.interp(
        time(),
        [2019.0, 2020.0, 2021.0, 2022.0, 2023.0],
        [89.85, 88.34, 89.55, 89.19, 88.54],
    )


@component.add(
    name="Kebutuhan air populasi",
    units="m*m*m/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "populasi_pulau": 1,
        "standard_kebutuha_air_per_kapita": 1,
        "hari_dalam_tahun": 1,
        "liter_ke_meter_kubik": 1,
    },
)
def kebutuhan_air_populasi():
    return (
        populasi_pulau()
        * standard_kebutuha_air_per_kapita()
        * hari_dalam_tahun()
        / liter_ke_meter_kubik()
    )


@component.add(
    name="Angkatan Kerja",
    units="jiwa",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"populasi_pulau": 1, "tpak_berbasis_populasi": 1},
)
def angkatan_kerja():
    return populasi_pulau() * tpak_berbasis_populasi()


@component.add(
    name="Intensitas penanaman",
    units="tahun/musim",
    comp_type="Constant",
    comp_subtype="Normal",
)
def intensitas_penanaman():
    return 2


@component.add(
    name="Rasio kecukupan air SK 146",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_ketersediaan_air_bisa_digunakan": 1,
        "total_kebutuhan_air_sk_146": 1,
    },
)
def rasio_kecukupan_air_sk_146():
    return total_ketersediaan_air_bisa_digunakan() / total_kebutuhan_air_sk_146()


@component.add(
    name="Rasio kecukupan pangan",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"biokapasitas_pangan": 1, "jejak_ekologis_pangan": 1},
)
def rasio_kecukupan_pangan():
    return biokapasitas_pangan() / jejak_ekologis_pangan()


@component.add(
    name="PDRB per kapita",
    units="JutaRp/(tahun*jiwa)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pdrb_pulau": 1, "populasi_pulau": 1},
)
def pdrb_per_kapita():
    return pdrb_pulau() / populasi_pulau()


@component.add(
    name="jumlah hari per musim tanam",
    units="hari/musim",
    comp_type="Constant",
    comp_subtype="Normal",
)
def jumlah_hari_per_musim_tanam():
    return 120


@component.add(
    name="Perubahan IKU Bali",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "iku_bali": 1,
        "elastisitas_perubahan_iku_bali": 1,
        "laju_pdrb_per_kapita": 1,
    },
)
def perubahan_iku_bali():
    return iku_bali() * elastisitas_perubahan_iku_bali() * laju_pdrb_per_kapita()


@component.add(
    name="Lahan Pangan per kapita",
    units="Ha/jiwa",
    comp_type="Constant",
    comp_subtype="Normal",
)
def lahan_pangan_per_kapita():
    """
    data n.a.
    """
    return 0.081


@component.add(
    name="Populasi Pulau",
    units="jiwa",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_populasi_pulau": 1},
    other_deps={
        "_integ_populasi_pulau": {
            "initial": {"populasi_historisprojeksi": 1},
            "step": {"pertumbuhan_populasi": 1},
        }
    },
)
def populasi_pulau():
    return _integ_populasi_pulau()


_integ_populasi_pulau = Integ(
    lambda: pertumbuhan_populasi(),
    lambda: populasi_historisprojeksi(),
    "_integ_populasi_pulau",
)


@component.add(
    name="Kebutuhan air per kapita",
    units="m*m*m/(tahun*jiwa)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def kebutuhan_air_per_kapita():
    """
    Falkenmark index
    """
    return 1700


@component.add(
    name="konverter detik ke jam",
    units="detik/jam",
    comp_type="Constant",
    comp_subtype="Normal",
)
def konverter_detik_ke_jam():
    return 3600


@component.add(
    name="Rasio kecukupan air Falkenmark",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ketersediaan_air_per_kapita": 1, "kebutuhan_air_per_kapita": 1},
)
def rasio_kecukupan_air_falkenmark():
    return ketersediaan_air_per_kapita() / kebutuhan_air_per_kapita()


@component.add(
    name="Elastisitas perubahan IKU Bali",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def elastisitas_perubahan_iku_bali():
    return np.interp(
        time(),
        [2018.0, 2019.0, 2020.0, 2021.0, 2022.0],
        [-0.12, 0.1882, -0.3945, -0.1119, -0.122],
    )


@component.add(
    name="Persentase air tercemar",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def persentase_air_tercemar():
    """
    dari proxy IKA 20192-2023
    """
    return np.interp(
        time(),
        [2019.0, 2020.0, 2021.0, 2022.0, 2023.0, 2045.0],
        [0.0735585, 0.0735585, 0.0735585, 0.0735585, 0.0735585, 0.0735585],
    )


@component.add(
    name='"std kebutuhan air per pertanian SK 146/2023"',
    units="m*m*m/detik/Ha",
    comp_type="Constant",
    comp_subtype="Normal",
)
def std_kebutuhan_air_per_pertanian_sk_1462023():
    return 0.001


@component.add(
    name="Ketersediaan air per kapita",
    units="m*m*m/(tahun*jiwa)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_ketersediaan_air_bisa_digunakan": 1, "populasi_pulau": 1},
)
def ketersediaan_air_per_kapita():
    return total_ketersediaan_air_bisa_digunakan() / populasi_pulau()


@component.add(
    name="konverter jam ke hari",
    units="jam/hari",
    comp_type="Constant",
    comp_subtype="Normal",
)
def konverter_jam_ke_hari():
    return 24


@component.add(
    name='"std kebutuhan air per kapita SK 146/2023"',
    units="m*m*m/(tahun*jiwa)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def std_kebutuhan_air_per_kapita_sk_1462023():
    """
    SK MenLHK 146/2023
    """
    return 42.3


@component.add(
    name="rasio air padi perkebunan",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def rasio_air_padi_perkebunan():
    return 4 / 1.5


@component.add(
    name="Jejak ekologis pangan",
    units="Ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"lahan_pangan_per_kapita": 1, "populasi_pulau": 1},
)
def jejak_ekologis_pangan():
    return lahan_pangan_per_kapita() * populasi_pulau()


@component.add(
    name="Laju PDRB Per kapita",
    units="Dmnl/tahun",
    comp_type="Stateful",
    comp_subtype="Trend",
    depends_on={"_trend_laju_pdrb_per_kapita": 1},
    other_deps={
        "_trend_laju_pdrb_per_kapita": {
            "initial": {
                "pdrb_per_kapita": 1,
                "waktu_meratakan_laju_pdrb_per_kapita": 1,
            },
            "step": {"pdrb_per_kapita": 1, "waktu_meratakan_laju_pdrb_per_kapita": 1},
        }
    },
)
def laju_pdrb_per_kapita():
    return _trend_laju_pdrb_per_kapita()


_trend_laju_pdrb_per_kapita = Trend(
    lambda: pdrb_per_kapita(),
    lambda: waktu_meratakan_laju_pdrb_per_kapita(),
    lambda: 0.05,
    "_trend_laju_pdrb_per_kapita",
)


@component.add(
    name="Supply air permukaan",
    units="m*m*m/tahun",
    comp_type="Constant",
    comp_subtype="Normal",
)
def supply_air_permukaan():
    """
    PUPR 2016 yang digunakan untuk D3TLH Air Nasional 2009 dan 2023
    """
    return 35346500000.0


@component.add(
    name='"std kebutuhan air per pertanian SK 146/2023 tahunan"',
    units="m*m*m/(Ha*tahun)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "konverter_detik_ke_jam": 1,
        "konverter_jam_ke_hari": 1,
        "jumlah_hari_per_musim_tanam": 1,
        "intensitas_penanaman": 1,
        "std_kebutuhan_air_per_pertanian_sk_1462023": 1,
    },
)
def std_kebutuhan_air_per_pertanian_sk_1462023_tahunan():
    return (
        konverter_detik_ke_jam()
        * konverter_jam_ke_hari()
        * jumlah_hari_per_musim_tanam()
        / intensitas_penanaman()
        * std_kebutuhan_air_per_pertanian_sk_1462023()
    )


@component.add(
    name="Potensi air tanah",
    units="m*m*m/tahun",
    comp_type="Constant",
    comp_subtype="Normal",
)
def potensi_air_tanah():
    return 11963000000.0


@component.add(
    name="Waktu meratakan laju PDRB per kapita",
    units="tahun",
    comp_type="Constant",
    comp_subtype="Normal",
)
def waktu_meratakan_laju_pdrb_per_kapita():
    return 1


@component.add(
    name="Total ketersediaan air bisa digunakan",
    units="m*m*m/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_ketersediaan_air": 1, "persentase_air_tercemar": 1},
)
def total_ketersediaan_air_bisa_digunakan():
    return total_ketersediaan_air() * (1 - persentase_air_tercemar())


@component.add(
    name="Air limbah industri ekonomi",
    units="m*m*m/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "alokasi_air_industri_ekonomi": 1,
        "fraksi_air_limbah_industri_ekonomi": 1,
    },
)
def air_limbah_industri_ekonomi():
    return alokasi_air_industri_ekonomi() * fraksi_air_limbah_industri_ekonomi()


@component.add(
    name="Air limbah rumah tangga",
    units="m*m*m/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"alokasi_air_populasi": 1, "fraksi_air_limbah_populasi": 1},
)
def air_limbah_rumah_tangga():
    return alokasi_air_populasi() * fraksi_air_limbah_populasi()


@component.add(
    name="fraksi air limbah industri ekonomi",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def fraksi_air_limbah_industri_ekonomi():
    return 0.75


@component.add(
    name="fraksi air limbah populasi",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def fraksi_air_limbah_populasi():
    return 0.8


@component.add(
    name="Fraksi jaringan air",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def fraksi_jaringan_air():
    return 0.2


@component.add(
    name="dampak kualitas air ke ekonomi table",
    units="Dmnl",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={"__lookup__": "_hardcodedlookup_dampak_kualitas_air_ke_ekonomi_table"},
)
def dampak_kualitas_air_ke_ekonomi_table(x, final_subs=None):
    return _hardcodedlookup_dampak_kualitas_air_ke_ekonomi_table(x, final_subs)


_hardcodedlookup_dampak_kualitas_air_ke_ekonomi_table = HardcodedLookups(
    [0.0, 1.0, 1.5, 2.0, 5.0, 10.0],
    [1.0, 1.0, 1.0, 0.9, 0.75, 0.5],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_dampak_kualitas_air_ke_ekonomi_table",
)


@component.add(
    name="dampak kualitas air ke industri ekonomi",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "rasio_konsentrasi_bod_thd_baku_mutu": 1,
        "dampak_kualitas_air_ke_ekonomi_table": 1,
    },
)
def dampak_kualitas_air_ke_industri_ekonomi():
    return dampak_kualitas_air_ke_ekonomi_table(rasio_konsentrasi_bod_thd_baku_mutu())


@component.add(
    name="Baku mutu BOD", units="mg/L", comp_type="Constant", comp_subtype="Normal"
)
def baku_mutu_bod():
    return 4


@component.add(
    name="BOD industri ekonomi",
    units="mg/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "air_limbah_industri_ekonomi": 1,
        "kandungan_bod_air_limbah_industri_ekonomi": 1,
        "liter_ke_meter_kubik": 1,
    },
)
def bod_industri_ekonomi():
    return (
        air_limbah_industri_ekonomi()
        * kandungan_bod_air_limbah_industri_ekonomi()
        * liter_ke_meter_kubik()
    )


@component.add(
    name="BOD rumah tangga",
    units="mg/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "air_limbah_rumah_tangga": 1,
        "kandungan_bod_rumah_tangga": 1,
        "liter_ke_meter_kubik": 1,
    },
)
def bod_rumah_tangga():
    return (
        air_limbah_rumah_tangga()
        * kandungan_bod_rumah_tangga()
        * liter_ke_meter_kubik()
    )


@component.add(
    name="BOD total",
    units="mg/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"bod_industri_ekonomi": 1, "bod_rumah_tangga": 1},
)
def bod_total():
    return bod_industri_ekonomi() + bod_rumah_tangga()


@component.add(
    name="delay dampak air ke ekonomi",
    units="tahun",
    comp_type="Constant",
    comp_subtype="Normal",
)
def delay_dampak_air_ke_ekonomi():
    return 2


@component.add(
    name="dampak kecukupan air industri ekonomi",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "kecukupan_air_industri_dan_ekonomi_delay": 1,
        "dampak_kecukupan_air_industri_ekonomi_table": 1,
    },
)
def dampak_kecukupan_air_industri_ekonomi():
    return dampak_kecukupan_air_industri_ekonomi_table(
        kecukupan_air_industri_dan_ekonomi_delay()
    )


@component.add(
    name="dampak kecukupan air industri ekonomi table",
    units="Dmnl",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={
        "__lookup__": "_hardcodedlookup_dampak_kecukupan_air_industri_ekonomi_table"
    },
)
def dampak_kecukupan_air_industri_ekonomi_table(x, final_subs=None):
    return _hardcodedlookup_dampak_kecukupan_air_industri_ekonomi_table(x, final_subs)


_hardcodedlookup_dampak_kecukupan_air_industri_ekonomi_table = HardcodedLookups(
    [0.0, 0.1, 0.281346, 0.40367, 0.5, 0.651376, 0.8, 0.9, 1.0],
    [0.0, 0.2, 0.447368, 0.605263, 0.7, 0.842105, 0.95, 1.0, 1.0],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_dampak_kecukupan_air_industri_ekonomi_table",
)


@component.add(
    name="Kandungan BOD rumah tangga",
    units="mg/L",
    comp_type="Constant",
    comp_subtype="Normal",
)
def kandungan_bod_rumah_tangga():
    """
    Natsir, 2021. ANALISIS KUALITAS BOD, COD, DAN TSS LIMBAH CAIR DOMESTIK (Grey Water) PADA RUMAH TANGGA DI KABUPATEN MAROS 2021. Vol. 4 No. 1 (2021): Jurnal Nasional Ilmu Kesehatan – Juni 2021
    """
    return 134.9


@component.add(
    name="rasio kecukupan air",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"suplai_air_jaringan": 1, "total_kebutuhan_air": 1},
)
def rasio_kecukupan_air():
    return suplai_air_jaringan() / total_kebutuhan_air()


@component.add(
    name="dampak kualitas air industri ekonomi delay",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Delay",
    depends_on={"_delay_dampak_kualitas_air_industri_ekonomi_delay": 1},
    other_deps={
        "_delay_dampak_kualitas_air_industri_ekonomi_delay": {
            "initial": {"delay_dampak_air_ke_ekonomi": 1},
            "step": {
                "dampak_kualitas_air_ke_industri_ekonomi": 1,
                "delay_dampak_air_ke_ekonomi": 1,
            },
        }
    },
)
def dampak_kualitas_air_industri_ekonomi_delay():
    return _delay_dampak_kualitas_air_industri_ekonomi_delay()


_delay_dampak_kualitas_air_industri_ekonomi_delay = Delay(
    lambda: dampak_kualitas_air_ke_industri_ekonomi(),
    lambda: delay_dampak_air_ke_ekonomi(),
    lambda: 1,
    lambda: 3,
    time_step,
    "_delay_dampak_kualitas_air_industri_ekonomi_delay",
)


@component.add(
    name="kecukupan air industri dan ekonomi delay",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Delay",
    depends_on={"_delay_kecukupan_air_industri_dan_ekonomi_delay": 1},
    other_deps={
        "_delay_kecukupan_air_industri_dan_ekonomi_delay": {
            "initial": {"delay_dampak_air_ke_ekonomi": 1},
            "step": {
                "kecukupan_air_industri_dan_ekonomi": 1,
                "delay_dampak_air_ke_ekonomi": 1,
            },
        }
    },
)
def kecukupan_air_industri_dan_ekonomi_delay():
    return _delay_kecukupan_air_industri_dan_ekonomi_delay()


_delay_kecukupan_air_industri_dan_ekonomi_delay = Delay(
    lambda: kecukupan_air_industri_dan_ekonomi(),
    lambda: delay_dampak_air_ke_ekonomi(),
    lambda: 1,
    lambda: 3,
    time_step,
    "_delay_kecukupan_air_industri_dan_ekonomi_delay",
)


@component.add(
    name="dampak kualitas air ke rumah tangga",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "rasio_konsentrasi_bod_thd_baku_mutu": 1,
        "dampak_kualitas_air_ke_rumah_tangga_table": 1,
    },
)
def dampak_kualitas_air_ke_rumah_tangga():
    return dampak_kualitas_air_ke_rumah_tangga_table(
        rasio_konsentrasi_bod_thd_baku_mutu()
    )


@component.add(
    name="dampak kualitas air ke rumah tangga delay",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Delay",
    depends_on={"_delay_dampak_kualitas_air_ke_rumah_tangga_delay": 1},
    other_deps={
        "_delay_dampak_kualitas_air_ke_rumah_tangga_delay": {
            "initial": {"delay_dampak_air": 1},
            "step": {"dampak_kualitas_air_ke_rumah_tangga": 1, "delay_dampak_air": 1},
        }
    },
)
def dampak_kualitas_air_ke_rumah_tangga_delay():
    return _delay_dampak_kualitas_air_ke_rumah_tangga_delay()


_delay_dampak_kualitas_air_ke_rumah_tangga_delay = Delay(
    lambda: dampak_kualitas_air_ke_rumah_tangga(),
    lambda: delay_dampak_air(),
    lambda: 1,
    lambda: 3,
    time_step,
    "_delay_dampak_kualitas_air_ke_rumah_tangga_delay",
)


@component.add(
    name="dampak kualitas air ke rumah tangga table",
    units="Dmnl",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={
        "__lookup__": "_hardcodedlookup_dampak_kualitas_air_ke_rumah_tangga_table"
    },
)
def dampak_kualitas_air_ke_rumah_tangga_table(x, final_subs=None):
    return _hardcodedlookup_dampak_kualitas_air_ke_rumah_tangga_table(x, final_subs)


_hardcodedlookup_dampak_kualitas_air_ke_rumah_tangga_table = HardcodedLookups(
    [0.0, 1.0, 2.0, 5.0, 10.0],
    [1.0, 1.0, 0.9, 0.65, 0.3],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_dampak_kualitas_air_ke_rumah_tangga_table",
)


@component.add(
    name="kecukupan air industri dan ekonomi",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "alokasi_air_industri_ekonomi": 1,
        "kebutuhan_air_industri_dan_ekonomi": 1,
    },
)
def kecukupan_air_industri_dan_ekonomi():
    return alokasi_air_industri_ekonomi() / kebutuhan_air_industri_dan_ekonomi()


@component.add(
    name="konsentrasi BOD",
    units="mg/L",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"bod_total": 1, "suplai_air_alamiahn": 1, "liter_ke_meter_kubik": 1},
)
def konsentrasi_bod():
    return bod_total() / suplai_air_alamiahn() / liter_ke_meter_kubik()


@component.add(
    name="Suplai air jaringan",
    units="m*m*m/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"suplai_air_alamiahn": 1, "fraksi_jaringan_air": 1},
)
def suplai_air_jaringan():
    return suplai_air_alamiahn() * fraksi_jaringan_air()


@component.add(
    name="Rasio konsentrasi BOD thd baku mutu",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"konsentrasi_bod": 1, "baku_mutu_bod": 1},
)
def rasio_konsentrasi_bod_thd_baku_mutu():
    return konsentrasi_bod() / baku_mutu_bod()


@component.add(
    name="Suplai air alamiahn",
    units="m*m*m/tahun",
    comp_type="Stateful",
    comp_subtype="Initial",
    depends_on={"_initial_suplai_air_alamiahn": 1},
    other_deps={
        "_initial_suplai_air_alamiahn": {
            "initial": {"farksi_suplai_air": 1, "total_kebutuhan_air": 1},
            "step": {},
        }
    },
)
def suplai_air_alamiahn():
    return _initial_suplai_air_alamiahn()


_initial_suplai_air_alamiahn = Initial(
    lambda: farksi_suplai_air() * total_kebutuhan_air(), "_initial_suplai_air_alamiahn"
)


@component.add(
    name="Kandungan BOD air limbah industri ekonomi",
    units="mg/L",
    comp_type="Constant",
    comp_subtype="Normal",
)
def kandungan_bod_air_limbah_industri_ekonomi():
    """
    Yuniarti dan Widayatno, 2012. Analisa Perubahan BOD, COD, dan TSS Limbah Cair Industri Tekstil Menggunakan Metode Elektrooksidasi-elektrokoagulasi Elektroda Fe-C dengan Sistem Semi Kontinyu. Rekayasa Hijau: Jurnal Teknologi Ramah Lingkungan Industri Tekstil
    """
    return 104.7


@component.add(
    name="Alokasi air industri ekonomi",
    units="m*m*m/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"kebutuhan_air_industri_dan_ekonomi": 1, "kecukupan_air": 1},
)
def alokasi_air_industri_ekonomi():
    return kebutuhan_air_industri_dan_ekonomi() * kecukupan_air()


@component.add(
    name="Alokasi air populasi",
    units="m*m*m/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"kecukupan_air": 1, "kebutuhan_air_populasi": 1},
)
def alokasi_air_populasi():
    return kecukupan_air() * kebutuhan_air_populasi()


@component.add(
    name="Angkatan Kerja Historis",
    units="jiwa",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def angkatan_kerja_historis():
    """
    ([(2010,2e+06)-(2022,3e+06)],(2010,2.24449e+06),(2011,2.2678e+06),(2012,2.2 9143e+06),(2013,2.31538e+06),(2014,2.31676e+06),(2015,2.37202e+06),(2016,2. 46304e+06),(2017,2.43445e+06),(2018,2.52536e+06),(2019,2.46623e+06),(2020,2 .56792e+06),(2021,2.44185e+06),(2022,2.37854e+06) )
    """
    return np.interp(
        time(),
        [
            2010.0,
            2011.0,
            2012.0,
            2013.0,
            2014.0,
            2015.0,
            2016.0,
            2017.0,
            2018.0,
            2019.0,
            2020.0,
            2021.0,
            2022.0,
            2023.0,
        ],
        [
            1089100.0,
            1152430.0,
            1132950.0,
            1152640.0,
            1165490.0,
            1201890.0,
            1216410.0,
            1239820.0,
            1329020.0,
            1350040.0,
            1421690.0,
            1457180.0,
            1477820.0,
            1577120.0,
        ],
    )


@component.add(
    name="Asumsi KOR awal", units="tahun", comp_type="Constant", comp_subtype="Normal"
)
def asumsi_kor_awal():
    return 3


@component.add(
    name="Capacity Utilization Factor",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def capacity_utilization_factor():
    """
    dikembangkan sebagai representasi dampak covid ke ekonomi, melalui penurunan capacity utilizatio factor di ekonomi reference: ...
    """
    return np.interp(
        time(),
        [
            2016.0,
            2017.0,
            2018.0,
            2019.0,
            2020.0,
            2021.0,
            2022.0,
            2023.0,
            2024.0,
            2030.0,
            2035.0,
        ],
        [1.0, 1.0, 1.0, 1.0, 0.94, 0.95, 0.99, 0.99, 1.0, 1.0, 1.0],
    )


@component.add(
    name="dampak kecukupan air populasi",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"kecukupan_air_delay": 1, "dampak_kecukupan_air_populasi_table": 1},
)
def dampak_kecukupan_air_populasi():
    return dampak_kecukupan_air_populasi_table(kecukupan_air_delay())


@component.add(
    name="dampak kecukupan air populasi table",
    units="Dmnl",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={"__lookup__": "_hardcodedlookup_dampak_kecukupan_air_populasi_table"},
)
def dampak_kecukupan_air_populasi_table(x, final_subs=None):
    return _hardcodedlookup_dampak_kecukupan_air_populasi_table(x, final_subs)


_hardcodedlookup_dampak_kecukupan_air_populasi_table = HardcodedLookups(
    [0.0, 0.1, 0.5, 0.691131, 0.816514, 0.9, 1.0],
    [0.03, 0.15, 0.6, 0.79386, 0.934211, 1.0, 1.0],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_dampak_kecukupan_air_populasi_table",
)


@component.add(
    name="delay dampak air", units="tahun", comp_type="Constant", comp_subtype="Normal"
)
def delay_dampak_air():
    return 5


@component.add(
    name="Depresiasi",
    units="miliarRp/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"kapital": 1, "umur_kapital_rata2": 1},
)
def depresiasi():
    return kapital() / umur_kapital_rata2()


@component.add(
    name="Elastisitas LPE thd perubahan teknologi historis",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def elastisitas_lpe_thd_perubahan_teknologi_historis():
    """
    Asumsi jika pertumbuhan ekonomi naik 5% maka perubahan teknologi naik 3%
    """
    return np.interp(
        time(), [2010.0, 2024.0, 2025.0, 2026.0, 2030.0], [0.37, 0.37, 0.37, 0.37, 0.37]
    )


@component.add(
    name="Farksi suplai air", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def farksi_suplai_air():
    return 50


@component.add(
    name="Gap Kapital",
    units="JutaRp",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"kapital_dibutuhkan": 1, "kapital": 1},
)
def gap_kapital():
    return np.maximum(0, kapital_dibutuhkan() - kapital())


@component.add(
    name="hari dalam tahun",
    units="hari/tahun",
    comp_type="Constant",
    comp_subtype="Normal",
)
def hari_dalam_tahun():
    return 365


@component.add(
    name="Intensitas air untuk ekonomi",
    units="L/JutaRp",
    comp_type="Constant",
    comp_subtype="Normal",
)
def intensitas_air_untuk_ekonomi():
    return 2000


@component.add(
    name="Intensitas kapital", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def intensitas_kapital():
    return 0.45


@component.add(
    name="Investasi",
    units="JutaRp/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"investasi_dibutuhkan": 1, "potensi_investasi": 1, "investasi_luar": 1},
)
def investasi():
    return np.minimum(investasi_dibutuhkan(), potensi_investasi()) + investasi_luar()


@component.add(
    name="Investasi dibutuhkan",
    units="JutaRp/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"gap_kapital": 1, "waktu_pemenuhan_investasi": 1},
)
def investasi_dibutuhkan():
    return gap_kapital() / waktu_pemenuhan_investasi()


@component.add(
    name="Investasi historis",
    units="JutaRp/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def investasi_historis():
    return np.interp(
        time(),
        [
            2014.0,
            2015.0,
            2016.0,
            2017.0,
            2018.0,
            2019.0,
            2020.0,
            2021.0,
            2022.0,
            2023.0,
        ],
        [
            12595400.0,
            13406000.0,
            14591600.0,
            16052900.0,
            16624300.0,
            23155600.0,
            26612000.0,
            28661400.0,
            40173200.0,
            34391900.0,
        ],
    )


@component.add(
    name="Investasi luar",
    units="JutaRp/tahun",
    comp_type="Constant",
    comp_subtype="Normal",
)
def investasi_luar():
    return 0


@component.add(
    name="kapital",
    units="JutaRp",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_kapital": 1},
    other_deps={
        "_integ_kapital": {
            "initial": {"kapital_awal": 1},
            "step": {"investasi": 1, "depresiasi": 1},
        }
    },
)
def kapital():
    return _integ_kapital()


_integ_kapital = Integ(
    lambda: investasi() - depresiasi(), lambda: kapital_awal(), "_integ_kapital"
)


@component.add(
    name="Kapital awal",
    units="JutaRp",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pdrb_pulau_awal": 1, "asumsi_kor_awal": 1},
)
def kapital_awal():
    return pdrb_pulau_awal() * asumsi_kor_awal()


@component.add(
    name="Kapital dibutuhkan",
    units="JutaRp",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "intensitas_kapital": 1,
        "target_pdrb_pulau": 1,
        "umur_kapital_rata2": 1,
        "r": 1,
    },
)
def kapital_dibutuhkan():
    return intensitas_kapital() * target_pdrb_pulau() / (1 / umur_kapital_rata2() + r())


@component.add(
    name="Kebutuhan air industri dan ekonomi",
    units="m*m*m/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pdrb_pulau": 1,
        "intensitas_air_untuk_ekonomi": 1,
        "liter_ke_meter_kubik": 1,
    },
)
def kebutuhan_air_industri_dan_ekonomi():
    return pdrb_pulau() * intensitas_air_untuk_ekonomi() / liter_ke_meter_kubik()


@component.add(
    name="Kecukupan air",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"suplai_air_jaringan": 1, "total_kebutuhan_air": 1},
)
def kecukupan_air():
    return np.minimum(1, suplai_air_jaringan() / total_kebutuhan_air())


@component.add(
    name="Kecukupan air delay",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Delay",
    depends_on={"_delay_kecukupan_air_delay": 1},
    other_deps={
        "_delay_kecukupan_air_delay": {
            "initial": {"delay_dampak_air": 1},
            "step": {"kecukupan_air_populasi": 1, "delay_dampak_air": 1},
        }
    },
)
def kecukupan_air_delay():
    return _delay_kecukupan_air_delay()


_delay_kecukupan_air_delay = Delay(
    lambda: kecukupan_air_populasi(),
    lambda: delay_dampak_air(),
    lambda: 1,
    lambda: 3,
    time_step,
    "_delay_kecukupan_air_delay",
)


@component.add(
    name="Kecukupan air populasi",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"alokasi_air_populasi": 1, "kebutuhan_air_populasi": 1},
)
def kecukupan_air_populasi():
    return alokasi_air_populasi() / kebutuhan_air_populasi()


@component.add(
    name="KLR Historis",
    units="JutaRp/jiwa",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"kapital": 1, "tenaga_kerja_historis": 1},
)
def klr_historis():
    return kapital() / tenaga_kerja_historis()


@component.add(
    name="KOR",
    units="tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"kapital": 1, "pdrb_pulau": 1},
)
def kor():
    return kapital() / pdrb_pulau()


@component.add(
    name="laju pertumbuhan populasi",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "satu_tahun_unit": 1, "laju_pertumbuhan_populasi_table": 1},
)
def laju_pertumbuhan_populasi():
    return laju_pertumbuhan_populasi_table(time() / satu_tahun_unit())


@component.add(
    name="laju pertumbuhan populasi table",
    units="1/tahun",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={"__lookup__": "_hardcodedlookup_laju_pertumbuhan_populasi_table"},
)
def laju_pertumbuhan_populasi_table(x, final_subs=None):
    return _hardcodedlookup_laju_pertumbuhan_populasi_table(x, final_subs)


_hardcodedlookup_laju_pertumbuhan_populasi_table = HardcodedLookups(
    [
        2010.0,
        2011.0,
        2012.0,
        2013.0,
        2014.0,
        2015.0,
        2016.0,
        2017.0,
        2018.0,
        2019.0,
        2020.0,
        2021.0,
        2022.0,
    ],
    [
        0.0272,
        0.0186,
        0.0203,
        0.02,
        0.0197,
        0.0194,
        0.0191,
        0.0188,
        0.0185,
        0.0174,
        0.0096,
        0.0105,
        0.0196,
    ],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_laju_pertumbuhan_populasi_table",
)


@component.add(
    name="liter ke meter kubik",
    units="L/(m*m*m)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def liter_ke_meter_kubik():
    return 1000


@component.add(
    name="LPE Pulau",
    units="1/tahun",
    comp_type="Stateful",
    comp_subtype="Trend",
    depends_on={"_trend_lpe_pulau": 1},
    other_deps={
        "_trend_lpe_pulau": {
            "initial": {
                "lpe_pulau_mulamula": 1,
                "pdrb_pulau": 1,
                "waktu_trend_lpe_pulau": 1,
            },
            "step": {"pdrb_pulau": 1, "waktu_trend_lpe_pulau": 1},
        }
    },
)
def lpe_pulau():
    return _trend_lpe_pulau()


_trend_lpe_pulau = Trend(
    lambda: pdrb_pulau(),
    lambda: waktu_trend_lpe_pulau(),
    lambda: lpe_pulau_mulamula(),
    "_trend_lpe_pulau",
)


@component.add(
    name="Lpe Pulau historis",
    units="Dmnl/tahun",
    comp_type="Stateful",
    comp_subtype="Trend",
    depends_on={"_trend_lpe_pulau_historis": 1},
    other_deps={
        "_trend_lpe_pulau_historis": {
            "initial": {
                "lpe_pulau_mulamula": 1,
                "pdrb_pulau_historis": 1,
                "waktu_trend_lpe_pulau": 1,
            },
            "step": {"pdrb_pulau_historis": 1, "waktu_trend_lpe_pulau": 1},
        }
    },
)
def lpe_pulau_historis():
    return _trend_lpe_pulau_historis()


_trend_lpe_pulau_historis = Trend(
    lambda: pdrb_pulau_historis(),
    lambda: waktu_trend_lpe_pulau(),
    lambda: lpe_pulau_mulamula(),
    "_trend_lpe_pulau_historis",
)


@component.add(
    name='"LPE Pulau Mula-mula"',
    units="1/tahun",
    comp_type="Constant",
    comp_subtype="Normal",
)
def lpe_pulau_mulamula():
    return 0.05


@component.add(
    name="mps",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def mps():
    """
    ([(2010,0.2)-(2030,0.4)],(2010,0.3),(2011,0.35),(2012,0.37),(2013,0.37),(20 14,0.36),(2015,0.37),(2016,0.37),(2017,0.36),(2018,0.37),(2019,0.36),(2020, 0.31),(2021,0.3),(2022,0.31),(2025,0.32),(2030,0.35) )
    """
    return np.interp(
        time(),
        [
            2014.0,
            2015.0,
            2016.0,
            2017.0,
            2018.0,
            2019.0,
            2020.0,
            2021.0,
            2022.0,
            2023.0,
            2027.0,
            2030.0,
        ],
        [
            0.294446,
            0.296334,
            0.305003,
            0.33,
            0.33,
            0.45,
            0.49,
            0.5,
            0.65,
            0.5,
            0.4,
            0.32,
        ],
    )


@component.add(
    name="PDRB Pulau awal",
    units="JutaRp/tahun",
    comp_type="Stateful",
    comp_subtype="Initial",
    depends_on={"_initial_pdrb_pulau_awal": 1},
    other_deps={
        "_initial_pdrb_pulau_awal": {"initial": {"pdrb_pulau_historis": 1}, "step": {}}
    },
)
def pdrb_pulau_awal():
    """
    PDRB ADHK Bali 2010
    """
    return _initial_pdrb_pulau_awal()


_initial_pdrb_pulau_awal = Initial(
    lambda: pdrb_pulau_historis(), "_initial_pdrb_pulau_awal"
)


@component.add(
    name="PDRB Pulau historis",
    units="JutaRp/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def pdrb_pulau_historis():
    return np.interp(
        time(),
        [
            2010.0,
            2011.0,
            2012.0,
            2013.0,
            2014.0,
            2015.0,
            2016.0,
            2017.0,
            2018.0,
            2019.0,
            2020.0,
            2021.0,
            2022.0,
            2023.0,
        ],
        [
            33412500.0,
            35599900.0,
            38120200.0,
            40309600.0,
            42776500.0,
            45239500.0,
            47840900.0,
            51025000.0,
            54491200.0,
            57647000.0,
            58797300.0,
            64619900.0,
            73823100.0,
            83817100.0,
        ],
    )


@component.add(
    name="PDRB Pulau rerata",
    units="JutaRp/tahun",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_pdrb_pulau_rerata": 1},
    other_deps={
        "_integ_pdrb_pulau_rerata": {
            "initial": {"pdrb_pulau_awal": 1},
            "step": {"perubahan_pdrb_pulau_rerata": 1},
        }
    },
)
def pdrb_pulau_rerata():
    return _integ_pdrb_pulau_rerata()


_integ_pdrb_pulau_rerata = Integ(
    lambda: perubahan_pdrb_pulau_rerata(),
    lambda: pdrb_pulau_awal(),
    "_integ_pdrb_pulau_rerata",
)


@component.add(
    name="pendapatan",
    units="JutaRp/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pdrb_pulau": 1},
)
def pendapatan():
    """
    PDB sisi Produksi (lapangan usaha), akan sama dengan PDB Pendapatan (income), dan penggunaan (consumptions)
    """
    return pdrb_pulau()


@component.add(
    name="pendapatan untuk digunakan",
    units="JutaRp/tahun",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_pendapatan_untuk_digunakan": 1},
    other_deps={
        "_smooth_pendapatan_untuk_digunakan": {
            "initial": {"pendapatan": 1},
            "step": {"pendapatan": 1, "waktu_meratakan_pendapatan": 1},
        }
    },
)
def pendapatan_untuk_digunakan():
    return _smooth_pendapatan_untuk_digunakan()


_smooth_pendapatan_untuk_digunakan = Smooth(
    lambda: pendapatan(),
    lambda: waktu_meratakan_pendapatan(),
    lambda: pendapatan(),
    lambda: 1,
    "_smooth_pendapatan_untuk_digunakan",
)


@component.add(
    name="Pengangguran",
    units="jiwa",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"angkatan_kerja": 1, "tenaga_kerja": 1},
)
def pengangguran():
    return angkatan_kerja() - tenaga_kerja()


@component.add(
    name="Pengangguran historis 2",
    units="jiwa",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"angkatan_kerja_historis": 1, "tenaga_kerja_historis": 1},
)
def pengangguran_historis_2():
    return angkatan_kerja_historis() - tenaga_kerja_historis()


@component.add(
    name='"Tk Pengangguran historis+projeksi table"',
    units="Dmnl",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={
        "__lookup__": "_hardcodedlookup_tk_pengangguran_historisprojeksi_table"
    },
)
def tk_pengangguran_historisprojeksi_table(x, final_subs=None):
    return _hardcodedlookup_tk_pengangguran_historisprojeksi_table(x, final_subs)


_hardcodedlookup_tk_pengangguran_historisprojeksi_table = HardcodedLookups(
    [
        2010.0,
        2011.0,
        2012.0,
        2013.0,
        2014.0,
        2015.0,
        2016.0,
        2017.0,
        2018.0,
        2019.0,
        2020.0,
        2021.0,
        2022.0,
        2023.0,
    ],
    [
        0.031,
        0.03,
        0.021,
        0.018,
        0.019,
        0.02,
        0.019,
        0.015,
        0.014,
        0.016,
        0.056,
        0.054,
        0.048,
        0.027,
    ],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_tk_pengangguran_historisprojeksi_table",
)


@component.add(
    name="Perubahan PDRB Pulau rerata",
    units="miliarRp/(tahun*tahun)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pdrb_pulau": 1,
        "pdrb_pulau_rerata": 1,
        "waktu_meratakan_pdrb_pulau": 1,
    },
)
def perubahan_pdrb_pulau_rerata():
    return (pdrb_pulau() - pdrb_pulau_rerata()) / waktu_meratakan_pdrb_pulau()


@component.add(
    name="Perubahan PDRB Pulau target",
    units="miliarRp/(tahun*tahun)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pdrb_pulau_rerata": 1, "target_lpe_pulau": 1},
)
def perubahan_pdrb_pulau_target():
    return pdrb_pulau_rerata() * target_lpe_pulau()


@component.add(
    name='"Populasi historis+Projeksi"',
    units="jiwa",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def populasi_historisprojeksi():
    return np.interp(
        time(),
        [
            2010.0,
            2011.0,
            2012.0,
            2013.0,
            2014.0,
            2015.0,
            2016.0,
            2017.0,
            2018.0,
            2019.0,
            2020.0,
            2021.0,
            2022.0,
            2023.0,
        ],
        [
            2571590.0,
            2641550.0,
            2690720.0,
            2745370.0,
            2800340.0,
            2855590.0,
            2911010.0,
            2966600.0,
            3022330.0,
            3078210.0,
            3131860.0,
            3161800.0,
            3194950.0,
            3257610.0,
        ],
    )


@component.add(
    name="Potensi investasi",
    units="JutaRp/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"tabungan": 1},
)
def potensi_investasi():
    return tabungan()


@component.add(name="r", units="1/tahun", comp_type="Constant", comp_subtype="Normal")
def r():
    """
    natural interest rate in cobb douglas or nathan forester model 1982
    """
    return 0.03


@component.add(
    name="satu tahun unit", units="tahun", comp_type="Constant", comp_subtype="Normal"
)
def satu_tahun_unit():
    return 1


@component.add(
    name="Sensitivitas tk teknologi thd KLR",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def sensitivitas_tk_teknologi_thd_klr():
    """
    ([(2010,0)-(2030,4)],(2010,2.4),(2019,2.4),(2023,4),(2030,2.7) )
    """
    return np.interp(
        time(),
        [2010.0, 2019.0, 2020.0, 2021.0, 2022.0, 2023.0, 2024.0, 2025.0, 2050.0],
        [2.5, 2.5, 2.7, 3.0, 3.0, 3.0, 2.8, 2.5, 2.2],
    )


@component.add(
    name="Standard kebutuha air per kapita",
    units="L/jiwa/hari",
    comp_type="Constant",
    comp_subtype="Normal",
)
def standard_kebutuha_air_per_kapita():
    return 200


@component.add(
    name="target LPE Pulau",
    units="1/tahun",
    comp_type="Constant",
    comp_subtype="Normal",
)
def target_lpe_pulau():
    return 0.07


@component.add(
    name="Target PDRB Pulau",
    units="JutaRp/tahun",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_target_pdrb_pulau": 1},
    other_deps={
        "_integ_target_pdrb_pulau": {
            "initial": {"pdrb_pulau_awal": 1},
            "step": {"perubahan_pdrb_pulau_target": 1},
        }
    },
)
def target_pdrb_pulau():
    return _integ_target_pdrb_pulau()


_integ_target_pdrb_pulau = Integ(
    lambda: perubahan_pdrb_pulau_target(),
    lambda: pdrb_pulau_awal(),
    "_integ_target_pdrb_pulau",
)


@component.add(
    name="Tenaga kerja awal",
    units="jiwa",
    comp_type="Stateful",
    comp_subtype="Initial",
    depends_on={"_initial_tenaga_kerja_awal": 1},
    other_deps={
        "_initial_tenaga_kerja_awal": {
            "initial": {"tenaga_kerja_historis": 1},
            "step": {},
        }
    },
)
def tenaga_kerja_awal():
    return _initial_tenaga_kerja_awal()


_initial_tenaga_kerja_awal = Initial(
    lambda: tenaga_kerja_historis(), "_initial_tenaga_kerja_awal"
)


@component.add(
    name="Tenaga Kerja historis",
    units="jiwa",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def tenaga_kerja_historis():
    """
    ([(2010,2e+06)-(2022,3e+06)],(2010,2.2004e+06),(2011,2.22463e+06),(2012,2.2 4913e+06),(2013,2.2739e+06),(2014,2.27263e+06),(2015,2.3248e+06),(2016,2.41 656e+06),(2017,2.39831e+06),(2018,2.49087e+06),(2019,2.42868e+06),(2020,2.4 2342e+06),(2021,2.30318e+06),(2022,2.24707e+06) )
    """
    return np.interp(
        time(),
        [
            2010.0,
            2011.0,
            2012.0,
            2013.0,
            2014.0,
            2015.0,
            2016.0,
            2017.0,
            2018.0,
            2019.0,
            2020.0,
            2021.0,
            2022.0,
            2023.0,
        ],
        [
            997791.0,
            1076580.0,
            1060550.0,
            1053770.0,
            1057670.0,
            1137610.0,
            1194260.0,
            1130780.0,
            1247570.0,
            1267590.0,
            1328200.0,
            1369450.0,
            1393810.0,
            1487950.0,
        ],
    )


@component.add(
    name="Tingkat Teknologi",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_tingkat_teknologi": 1},
    other_deps={
        "_integ_tingkat_teknologi": {
            "initial": {},
            "step": {"perubahan_tk_teknologi": 1},
        }
    },
)
def tingkat_teknologi():
    return _integ_tingkat_teknologi()


_integ_tingkat_teknologi = Integ(
    lambda: perubahan_tk_teknologi(), lambda: 1, "_integ_tingkat_teknologi"
)


@component.add(
    name="Tk Pengangguran historis",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pengangguran_historis_2": 1, "angkatan_kerja_historis": 1},
)
def tk_pengangguran_historis():
    return pengangguran_historis_2() / angkatan_kerja_historis()


@component.add(
    name="Total kebutuhan air",
    units="m*m*m/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"kebutuhan_air_populasi": 1, "kebutuhan_air_industri_dan_ekonomi": 1},
)
def total_kebutuhan_air():
    return kebutuhan_air_populasi() + kebutuhan_air_industri_dan_ekonomi()


@component.add(
    name="TPAK berbasis populasi",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "satu_tahun_unit": 1, "tpak_berbasis_populasi_table": 1},
)
def tpak_berbasis_populasi():
    return tpak_berbasis_populasi_table(time() / satu_tahun_unit())


@component.add(
    name="TPAK berbasis populasi table",
    units="Dmnl",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={"__lookup__": "_hardcodedlookup_tpak_berbasis_populasi_table"},
)
def tpak_berbasis_populasi_table(x, final_subs=None):
    return _hardcodedlookup_tpak_berbasis_populasi_table(x, final_subs)


_hardcodedlookup_tpak_berbasis_populasi_table = HardcodedLookups(
    [
        2010.0,
        2011.0,
        2012.0,
        2013.0,
        2014.0,
        2015.0,
        2016.0,
        2017.0,
        2018.0,
        2019.0,
        2020.0,
        2021.0,
        2022.0,
        2023.0,
    ],
    [
        0.4235,
        0.4363,
        0.4211,
        0.4198,
        0.4162,
        0.4209,
        0.4179,
        0.4179,
        0.4397,
        0.4386,
        0.4539,
        0.4609,
        0.4625,
        0.4841,
    ],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_tpak_berbasis_populasi_table",
)


@component.add(
    name="umur kapital rata2",
    units="tahun",
    comp_type="Constant",
    comp_subtype="Normal",
)
def umur_kapital_rata2():
    return 25


@component.add(
    name="Waktu meratakan PDRB Pulau",
    units="tahun",
    comp_type="Constant",
    comp_subtype="Normal",
)
def waktu_meratakan_pdrb_pulau():
    return 0.5


@component.add(
    name="waktu meratakan pendapatan",
    units="tahun",
    comp_type="Constant",
    comp_subtype="Normal",
)
def waktu_meratakan_pendapatan():
    return 2


@component.add(
    name="Waktu pemenuhan investasi",
    units="tahun",
    comp_type="Constant",
    comp_subtype="Normal",
)
def waktu_pemenuhan_investasi():
    return 3


@component.add(
    name="Waktu Trend LPE Pulau",
    units="tahun",
    comp_type="Constant",
    comp_subtype="Normal",
)
def waktu_trend_lpe_pulau():
    return 1
