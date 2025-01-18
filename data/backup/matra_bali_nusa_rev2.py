"""
Python model 'matra_bali_nusa_rev2.py'
Translated using PySD
"""

from pathlib import Path
import numpy as np

from pysd.py_backend.functions import step, if_then_else, not_implemented_function
from pysd.py_backend.statefuls import Initial, Integ, Smooth, Trend, Delay
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
    "time_step": lambda: 1,
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
    name="Tabungan",
    units="JutaRp/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"mps_historical_and_policy": 1, "pendapatan_untuk_digunakan": 1},
)
def tabungan():
    return mps_historical_and_policy() * pendapatan_untuk_digunakan()


@component.add(
    name="Impact migrasi dari ekonomi",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "switch_impact_migrasi_dari_ekonomi": 1,
        "rasio_pdrb_per_kapita_to_2023": 1,
        "power_impact_migrasi_dari_ekonomi": 1,
    },
)
def impact_migrasi_dari_ekonomi():
    return if_then_else(
        switch_impact_migrasi_dari_ekonomi() == 0,
        lambda: 1,
        lambda: np.maximum(
            rasio_pdrb_per_kapita_to_2023() ** power_impact_migrasi_dari_ekonomi(), 1
        ),
    )


@component.add(
    name="Pertumbuhan populasi",
    units="jiwa/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "populasi_pulau": 1,
        "lpp_historis_dan_policy": 1,
        "impact_migrasi_dari_ekonomi": 1,
    },
)
def pertumbuhan_populasi():
    return populasi_pulau() * lpp_historis_dan_policy() * impact_migrasi_dari_ekonomi()


@component.add(
    name="Switch Impact migrasi dari ekonomi",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def switch_impact_migrasi_dari_ekonomi():
    return 0


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
    name="rasio tenaga kerja",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"tenaga_kerja": 1, "tenaga_kerja_awal": 1},
)
def rasio_tenaga_kerja():
    return tenaga_kerja() / tenaga_kerja_awal()


@component.add(
    name="Elastisitas LPE thd perubahan teknologi",
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
    name="Elastisitas LPE thd perubahan teknologi target",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def elastisitas_lpe_thd_perubahan_teknologi_target():
    return 0.35


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
    name="perubahan Elastisitas LPE thd perubahan teknologi delay",
    units="1",
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
    name="time to change Elastisitas LPE thd perubahan teknologi",
    units="tahun",
    comp_type="Constant",
    comp_subtype="Normal",
)
def time_to_change_elastisitas_lpe_thd_perubahan_teknologi():
    return 3000


@component.add(
    name="delay on change Elastisitas LPE thd perubahan teknologi",
    units="tahun",
    comp_type="Constant",
    comp_subtype="Normal",
)
def delay_on_change_elastisitas_lpe_thd_perubahan_teknologi():
    return 7


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
        "switch_perubahan_lahan_per_kapita": 1,
        "laju_perubahan_lahan_terbangun_per_kapita_historis_and_policy": 1,
        "laju_pdrb_per_kapita": 1,
        "elasticity_pdrb_per_kapita_to_unit_lahan_terbangun": 1,
        "lahan_terbangun_per_kapita": 1,
    },
)
def perubahan_lahan_terbangun_per_kapita():
    return (
        if_then_else(
            switch_perubahan_lahan_per_kapita() == 0,
            lambda: laju_perubahan_lahan_terbangun_per_kapita_historis_and_policy(),
            lambda: laju_pdrb_per_kapita()
            * elasticity_pdrb_per_kapita_to_unit_lahan_terbangun(),
        )
        * lahan_terbangun_per_kapita()
    )


@component.add(
    name="delay on perubahan Laju Perubahan Lahan Terbangun per Kapita",
    units="tahun",
    comp_type="Constant",
    comp_subtype="Normal",
)
def delay_on_perubahan_laju_perubahan_lahan_terbangun_per_kapita():
    return 5


@component.add(
    name="time to change Laju Perubahan Lahan Terbangun per Kapita",
    units="tahun",
    comp_type="Constant",
    comp_subtype="Normal",
)
def time_to_change_laju_perubahan_lahan_terbangun_per_kapita():
    return 3000


@component.add(
    name="Laju Perubahan Lahan Terbangun per Kapita historis and policy",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "laju_perubahan_lahan_terbangun_per_kapita": 1,
        "perubahan_laju_perubahan_lahan_terbangun_per_kapita_delay": 1,
    },
)
def laju_perubahan_lahan_terbangun_per_kapita_historis_and_policy():
    return (
        laju_perubahan_lahan_terbangun_per_kapita()
        + perubahan_laju_perubahan_lahan_terbangun_per_kapita_delay()
    )


@component.add(
    name="Laju Perubahan Lahan Terbangun per Kapita asumsi",
    units="1/tahun",
    comp_type="Constant",
    comp_subtype="Normal",
)
def laju_perubahan_lahan_terbangun_per_kapita_asumsi():
    return 0.03


@component.add(
    name="perubahan Laju Perubahan Lahan Terbangun per Kapita delay",
    units="1/tahun",
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
    name="mps historical and policy",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"mps": 1, "mps_change_delay": 1},
)
def mps_historical_and_policy():
    return mps() + mps_change_delay()


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
    name="laju pertumbuhan populasi asumsi",
    units="1/tahun",
    comp_type="Constant",
    comp_subtype="Normal",
)
def laju_pertumbuhan_populasi_asumsi():
    return 0.0116116


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
    units="1/tahun",
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
    name="mps assumption", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def mps_assumption():
    return 0.36


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
    name="time to change mps assumption",
    units="tahun",
    comp_type="Constant",
    comp_subtype="Normal",
)
def time_to_change_mps_assumption():
    return 3000


@component.add(
    name="time to change laju pertumbuhan populasi asumsi",
    units="tahun",
    comp_type="Constant",
    comp_subtype="Normal",
)
def time_to_change_laju_pertumbuhan_populasi_asumsi():
    return 3000


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
    name="Biokapasitas Pangan",
    units="Ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_lahan": 1,
        "pertambangan": 1,
        "lahan_lainnya": 1,
        "lahan_terbangun": 1,
        "fraksi_lahan_pangan_dimanfaatkan": 1,
    },
)
def biokapasitas_pangan():
    return (
        total_lahan() - pertambangan() - lahan_lainnya() - lahan_terbangun()
    ) * fraksi_lahan_pangan_dimanfaatkan()


@component.add(
    name="persentase lahan utk biokapasitas pangan",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"biokapasitas_pangan": 1, "total_lahan": 1},
)
def persentase_lahan_utk_biokapasitas_pangan():
    return biokapasitas_pangan() / total_lahan()


@component.add(
    name="Fraksi lahan pangan dimanfaatkan",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def fraksi_lahan_pangan_dimanfaatkan():
    return 0.787


@component.add(
    name="Jejak ekologis tempat ginggal",
    units="Ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"lahan_builtup_per_kapita": 1, "populasi_pulau": 1},
)
def jejak_ekologis_tempat_ginggal():
    return lahan_builtup_per_kapita() * populasi_pulau()


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
    name='"Lahan built-up per kapita"',
    units="Ha/jiwa",
    comp_type="Constant",
    comp_subtype="Normal",
)
def lahan_builtup_per_kapita():
    return 0.0024956


@component.add(
    name="Rasio Kecukupan lahan tempat tinggal",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"biokapasitas_tempat_tinggal": 1, "jejak_ekologis_tempat_ginggal": 1},
)
def rasio_kecukupan_lahan_tempat_tinggal():
    return biokapasitas_tempat_tinggal() / jejak_ekologis_tempat_ginggal()


@component.add(
    name="Ambang Batas penduduk tempat tinggal",
    units="jiwa",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"biokapasitas_tempat_tinggal": 1, "lahan_builtup_per_kapita": 1},
)
def ambang_batas_penduduk_tempat_tinggal():
    return biokapasitas_tempat_tinggal() / lahan_builtup_per_kapita()


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
    name="koefisien I perkebunan",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def koefisien_i_perkebunan():
    return 1.5


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
    return 1


@component.add(
    name='"faktor koreksi kebutuhan air per kap SK 146/2023"',
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def faktor_koreksi_kebutuhan_air_per_kap_sk_1462023():
    return 2


@component.add(
    name="kebutuhan air pertanian SK 146",
    units="m*m*m/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pertanian": 1,
        "std_kebutuhan_air_per_pertanian_dasar_sk_1462023_tahunan": 1,
        "koefisien_i_persawahan": 1,
    },
)
def kebutuhan_air_pertanian_sk_146():
    return (
        pertanian()
        * std_kebutuhan_air_per_pertanian_dasar_sk_1462023_tahunan()
        * koefisien_i_persawahan()
    )


@component.add(
    name='"std kebutuhan air per perkebunan SK 146/2023 tahunan"',
    units="m*m*m/(Ha*tahun)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "std_kebutuhan_air_per_pertanian_dasar_sk_1462023_tahunan": 1,
        "koefisien_i_perkebunan": 1,
    },
)
def std_kebutuhan_air_per_perkebunan_sk_1462023_tahunan():
    return (
        std_kebutuhan_air_per_pertanian_dasar_sk_1462023_tahunan()
        * koefisien_i_perkebunan()
    )


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
    return kebutuhan_air_perkebunan_sk_146() + kebutuhan_air_pertanian_sk_146()


@component.add(
    name="koefisien I pertanian lahan kering campur",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def koefisien_i_pertanian_lahan_kering_campur():
    return 1


@component.add(
    name="Rasio PDRB Per kapita to 2023",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"rasio_pdrb_per_kapita": 1, "rasio_pdrb_per_kapita_2023": 1},
)
def rasio_pdrb_per_kapita_to_2023():
    return rasio_pdrb_per_kapita() / rasio_pdrb_per_kapita_2023()


@component.add(
    name="power Impact migrasi dari ekonomi",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def power_impact_migrasi_dari_ekonomi():
    return 0.2


@component.add(
    name="Rasio PDRB Per kapita",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pdrb_per_kapita": 1, "pdrb_per_kapita_awal": 1},
)
def rasio_pdrb_per_kapita():
    return pdrb_per_kapita() / pdrb_per_kapita_awal()


@component.add(
    name="Rasio PDRB Per kapita 2023",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def rasio_pdrb_per_kapita_2023():
    return 1.12


@component.add(
    name="PDRB Per kapita awal",
    units="JutaRp/(jiwa*tahun)",
    comp_type="Stateful",
    comp_subtype="Initial",
    depends_on={"_initial_pdrb_per_kapita_awal": 1},
    other_deps={
        "_initial_pdrb_per_kapita_awal": {"initial": {"pdrb_per_kapita": 1}, "step": {}}
    },
)
def pdrb_per_kapita_awal():
    return _initial_pdrb_per_kapita_awal()


_initial_pdrb_per_kapita_awal = Initial(
    lambda: pdrb_per_kapita(), "_initial_pdrb_per_kapita_awal"
)


@component.add(
    name="Ambang Batas Air",
    units="jiwa",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_ketersediaan_air_bisa_digunakan": 1,
        "kebutuhan_air_per_kapita": 1,
    },
)
def ambang_batas_air():
    return total_ketersediaan_air_bisa_digunakan() / kebutuhan_air_per_kapita()


@component.add(
    name="Switch perubahan lahan per kapita",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def switch_perubahan_lahan_per_kapita():
    return 0


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
    name="Elasticity PDRB per kapita to unit lahan terbangun",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def elasticity_pdrb_per_kapita_to_unit_lahan_terbangun():
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
            2040.0,
            2050.0,
        ],
        [
            8.213,
            4.22366,
            12.2694,
            2.36034,
            -2.00101,
            7.11036,
            3.07789,
            2.43519,
            1.08468,
            0.45,
            0.32,
            0.8,
        ],
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
    name="Belukar Padang Rumput to Lahan Terbangun",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "belukar_padang_rumput_to_lahan_terbangun_indicated": 1,
        "availability_effect_belukar_padang_rumput": 1,
    },
)
def belukar_padang_rumput_to_lahan_terbangun():
    return (
        belukar_padang_rumput_to_lahan_terbangun_indicated()
        * availability_effect_belukar_padang_rumput()
    )


@component.add(
    name="Pertanian to Lahan Terbangun",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pertanian_to_lahan_terbangun_indicated": 1,
        "availability_effect_pertanian": 1,
    },
)
def pertanian_to_lahan_terbangun():
    return pertanian_to_lahan_terbangun_indicated() * availability_effect_pertanian()


@component.add(
    name="Perkebunan to Lahan Terbangun",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "perkebunan_to_lahan_terbangun_indicated": 1,
        "availability_effect_perkebunan": 1,
    },
)
def perkebunan_to_lahan_terbangun():
    return perkebunan_to_lahan_terbangun_indicated() * availability_effect_perkebunan()


@component.add(
    name="Hutan Mangrove to Lahan Terbangun",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hutan_mangrove_to_lahan_terbangun_indicated": 1,
        "availability_effect_hutan_mangrove": 1,
    },
)
def hutan_mangrove_to_lahan_terbangun():
    return (
        hutan_mangrove_to_lahan_terbangun_indicated()
        * availability_effect_hutan_mangrove()
    )


@component.add(
    name='"Rawa & Badan Air ke Lahan Terbangun"',
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "rawa_badan_air_ke_lahan_terbangun_indicated": 1,
        "availability_effect_rawa_badan_air": 1,
    },
)
def rawa_badan_air_ke_lahan_terbangun():
    return (
        rawa_badan_air_ke_lahan_terbangun_indicated()
        * availability_effect_rawa_badan_air()
    )


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
    name='"Hutan Primer & Hutan Sekunder to Lahan Terbangun"',
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hutan_primer_hutan_sekunder_to_lahan_terbangun_indicated": 1,
        "availability_effect_hutan_dan_belukar": 1,
    },
)
def hutan_primer_hutan_sekunder_to_lahan_terbangun():
    return (
        hutan_primer_hutan_sekunder_to_lahan_terbangun_indicated()
        * availability_effect_hutan_dan_belukar()
    )


@component.add(
    name="Hutan Tanaman to Lahan Terbangun",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hutan_tanaman_to_lahan_terbangun_indicated": 1,
        "availability_effect_hutan_tanaman": 1,
    },
)
def hutan_tanaman_to_lahan_terbangun():
    return (
        hutan_tanaman_to_lahan_terbangun_indicated()
        * availability_effect_hutan_tanaman()
    )


@component.add(name="mult", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def mult():
    return 1.25


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
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0, 2023.0],
        [0.0806, 0.0338, 0.0582, 0.0227, 0.0285, 0.0077, 0.0249, 0.0366],
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
    name="Kebutuhan Lahan Terbangun",
    units="Ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"lahan_terbangun_per_kapita": 1, "populasi_pulau": 1},
)
def kebutuhan_lahan_terbangun():
    return lahan_terbangun_per_kapita() * populasi_pulau()


@component.add(
    name="Pertanian to Perkebunan Hist",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def pertanian_to_perkebunan_hist():
    return np.interp(
        time(),
        [
            2016,
            2018,
            2019,
            2021,
            2022,
            2024,
            2025,
            2029,
            2030,
            2034,
            2035,
            2039,
            2040,
            2044,
            2045,
            2049,
            2050,
            2054,
            2055,
        ],
        [526, 526, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    )


@component.add(
    name="Lahan Terbangun to Perkebunan Hist",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def lahan_terbangun_to_perkebunan_hist():
    return np.interp(
        time(),
        [
            2016,
            2018,
            2019,
            2021,
            2022,
            2024,
            2025,
            2029,
            2030,
            2034,
            2035,
            2039,
            2040,
            2044,
            2045,
            2049,
            2050,
            2054,
            2055,
        ],
        [14, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    )


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
    return np.interp(
        time(),
        [
            2016,
            2018,
            2019,
            2021,
            2022,
            2024,
            2025,
            2029,
            2030,
            2034,
            2035,
            2039,
            2040,
            2044,
            2045,
            2049,
            2050,
            2054,
            2055,
        ],
        [3070, 3070, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    )


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
        [
            2016,
            2018,
            2019,
            2021,
            2022,
            2024,
            2025,
            2029,
            2030,
            2034,
            2035,
            2039,
            2040,
            2044,
            2045,
            2049,
            2050,
            2054,
            2055,
        ],
        [
            5211,
            5211,
            4416,
            4416,
            10444,
            10444,
            12950,
            12950,
            18079,
            18079,
            12598,
            12598,
            6872,
            6872,
            5606,
            5606,
            4621,
            4621,
            4621,
        ],
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
    return np.interp(
        time(),
        [
            2016,
            2018,
            2019,
            2021,
            2022,
            2024,
            2025,
            2029,
            2030,
            2034,
            2035,
            2039,
            2040,
            2044,
            2045,
            2049,
            2050,
            2054,
            2055,
        ],
        [51, 51, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    )


@component.add(
    name="Pertambangan ke Lahan Terbangun Hist",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def pertambangan_ke_lahan_terbangun_hist():
    return np.interp(
        time(),
        [
            2016,
            2018,
            2019,
            2021,
            2022,
            2024,
            2025,
            2029,
            2030,
            2034,
            2035,
            2039,
            2040,
            2044,
            2045,
            2049,
            2050,
            2054,
            2055,
        ],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
        time(),
        [
            2016,
            2018,
            2019,
            2021,
            2022,
            2024,
            2025,
            2029,
            2030,
            2034,
            2035,
            2039,
            2040,
            2044,
            2045,
            2049,
            2050,
            2054,
            2055,
        ],
        [15, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
        [
            2016,
            2018,
            2019,
            2021,
            2022,
            2024,
            2025,
            2029,
            2030,
            2034,
            2035,
            2039,
            2040,
            2044,
            2045,
            2049,
            2050,
            2054,
            2055,
        ],
        [
            5955,
            5955,
            6301,
            6301,
            10344,
            10344,
            9893,
            9893,
            6812,
            6812,
            6475,
            6475,
            5139,
            5139,
            4216,
            4216,
            5750,
            5750,
            5750,
        ],
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
    return np.interp(
        time(),
        [
            2016,
            2018,
            2019,
            2021,
            2022,
            2024,
            2025,
            2029,
            2030,
            2034,
            2035,
            2039,
            2040,
            2044,
            2045,
            2049,
            2050,
            2054,
            2055,
        ],
        [
            503,
            503,
            0,
            0,
            1165,
            1165,
            1049,
            1049,
            1435,
            1435,
            1316,
            1316,
            1025,
            1025,
            750,
            750,
            594,
            594,
            594,
        ],
    )


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
    return np.interp(
        time(),
        [
            2016,
            2018,
            2019,
            2021,
            2022,
            2024,
            2025,
            2029,
            2030,
            2034,
            2035,
            2039,
            2040,
            2044,
            2045,
            2049,
            2050,
            2054,
            2055,
        ],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    )


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
        [
            2016,
            2018,
            2019,
            2021,
            2022,
            2024,
            2025,
            2029,
            2030,
            2034,
            2035,
            2039,
            2040,
            2044,
            2045,
            2049,
            2050,
            2054,
            2055,
        ],
        [45, 45, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
    return np.interp(
        time(),
        [
            2016,
            2018,
            2019,
            2021,
            2022,
            2024,
            2025,
            2029,
            2030,
            2034,
            2035,
            2039,
            2040,
            2044,
            2045,
            2049,
            2050,
            2054,
            2055,
        ],
        [
            45189,
            45189,
            47363,
            47363,
            78038,
            78038,
            54675,
            54675,
            29855,
            29855,
            16320,
            16320,
            10260,
            10260,
            9754,
            9754,
            9005,
            9005,
            9005,
        ],
    )


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
    return np.interp(
        time(),
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            0.00046,
            0.00035,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
    )


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
    return np.interp(
        time(),
        [
            2016,
            2018,
            2019,
            2021,
            2022,
            2024,
            2025,
            2029,
            2030,
            2034,
            2035,
            2039,
            2040,
            2044,
            2045,
            2049,
            2050,
            2054,
            2055,
        ],
        [
            182,
            182,
            0,
            0,
            0,
            0,
            0,
            0,
            600,
            600,
            685,
            685,
            434,
            434,
            323,
            323,
            391,
            391,
            391,
        ],
    )


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
    return np.interp(
        time(),
        [
            2016,
            2018,
            2019,
            2021,
            2022,
            2024,
            2025,
            2029,
            2030,
            2034,
            2035,
            2039,
            2040,
            2044,
            2045,
            2049,
            2050,
            2054,
            2055,
        ],
        [3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    )


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
        time(),
        [
            2016,
            2018,
            2019,
            2021,
            2022,
            2024,
            2025,
            2029,
            2030,
            2034,
            2035,
            2039,
            2040,
            2044,
            2045,
            2049,
            2050,
            2054,
            2055,
        ],
        [21, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
    return np.interp(
        time(),
        [
            2016,
            2018,
            2019,
            2021,
            2022,
            2024,
            2025,
            2029,
            2030,
            2034,
            2035,
            2039,
            2040,
            2044,
            2045,
            2049,
            2050,
            2054,
            2055,
        ],
        [
            57822,
            57822,
            49089,
            49089,
            5669,
            5669,
            7168,
            7168,
            7048,
            7048,
            5299,
            5299,
            3990,
            3990,
            3524,
            3524,
            2903,
            2903,
            2903,
        ],
    )


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
    name="Laju Perubahan Lahan Terbangun per Kapita",
    units="1/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def laju_perubahan_lahan_terbangun_per_kapita():
    return np.interp(
        time(),
        [2016.0, 2017.0, 2018.0, 2019.0, 2020.0, 2021.0, 2022.0, 2025.0],
        [0.205325, 0.164053, 0.136615, 0.115691, 0.122478, 0.091922, 0.113174, 0.03],
    )


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
    return np.interp(
        time(),
        [
            2016,
            2018,
            2019,
            2021,
            2022,
            2024,
            2025,
            2029,
            2030,
            2034,
            2035,
            2039,
            2040,
            2044,
            2045,
            2049,
            2050,
            2054,
            2055,
        ],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    )


@component.add(
    name="Hutan Tanaman to Perkebunan Hist",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def hutan_tanaman_to_perkebunan_hist():
    return np.interp(
        time(),
        [
            2016,
            2018,
            2019,
            2021,
            2022,
            2024,
            2025,
            2029,
            2030,
            2034,
            2035,
            2039,
            2040,
            2044,
            2045,
            2049,
            2050,
            2054,
            2055,
        ],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    )


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
    return np.interp(
        time(),
        [
            2016,
            2018,
            2019,
            2021,
            2022,
            2024,
            2025,
            2029,
            2030,
            2034,
            2035,
            2039,
            2040,
            2044,
            2045,
            2049,
            2050,
            2054,
            2055,
        ],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    )


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
    return np.interp(
        time(),
        [
            2016,
            2018,
            2019,
            2021,
            2022,
            2024,
            2025,
            2029,
            2030,
            2034,
            2035,
            2039,
            2040,
            2044,
            2045,
            2049,
            2050,
            2054,
            2055,
        ],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    )


@component.add(
    name="Lahan Lainnya ke Lahan Terbangun Hist",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def lahan_lainnya_ke_lahan_terbangun_hist():
    return np.interp(
        time(),
        [
            2016,
            2018,
            2019,
            2021,
            2022,
            2024,
            2025,
            2029,
            2030,
            2034,
            2035,
            2039,
            2040,
            2044,
            2045,
            2049,
            2050,
            2054,
            2055,
        ],
        [99, 99, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    )


@component.add(
    name="Hutan Mangrove to Pertanian Hist",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def hutan_mangrove_to_pertanian_hist():
    return np.interp(
        time(),
        [
            2016,
            2018,
            2019,
            2021,
            2022,
            2024,
            2025,
            2029,
            2030,
            2034,
            2035,
            2039,
            2040,
            2044,
            2045,
            2049,
            2050,
            2054,
            2055,
        ],
        [383, 383, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    )


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
        [
            2016,
            2018,
            2019,
            2021,
            2022,
            2024,
            2025,
            2029,
            2030,
            2034,
            2035,
            2039,
            2040,
            2044,
            2045,
            2049,
            2050,
            2054,
            2055,
        ],
        [
            29893,
            29893,
            27692,
            27692,
            28929,
            28929,
            22394,
            22394,
            19512,
            19512,
            14396,
            14396,
            11665,
            11665,
            9322,
            9322,
            7223,
            7223,
            7223,
        ],
    )


@component.add(
    name="Pertambangan ke Pertanian Hist",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def pertambangan_ke_pertanian_hist():
    return np.interp(
        time(),
        [
            2016,
            2018,
            2019,
            2021,
            2022,
            2024,
            2025,
            2029,
            2030,
            2034,
            2035,
            2039,
            2040,
            2044,
            2045,
            2049,
            2050,
            2054,
            2055,
        ],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    )


@component.add(
    name="Lahan Lainnya ke Perkebunan Hist",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def lahan_lainnya_ke_perkebunan_hist():
    return np.interp(
        time(),
        [
            2016,
            2018,
            2019,
            2021,
            2022,
            2024,
            2025,
            2029,
            2030,
            2034,
            2035,
            2039,
            2040,
            2044,
            2045,
            2049,
            2050,
            2054,
            2055,
        ],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    )


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
    return 0.0117


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
        time(),
        [
            2016,
            2018,
            2019,
            2021,
            2022,
            2024,
            2025,
            2029,
            2030,
            2034,
            2035,
            2039,
            2040,
            2044,
            2045,
            2049,
            2050,
            2054,
            2055,
        ],
        [62, 62, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
    name="Pertambangan ke Lahan Terbangun",
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pertambangan_ke_lahan_terbangun_share": 1,
        "availability_effect_pertambangan": 1,
        "pertambangan": 1,
    },
)
def pertambangan_ke_lahan_terbangun():
    return (
        pertambangan_ke_lahan_terbangun_share()
        * availability_effect_pertambangan()
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
        "availability_effect_hutan_dan_belukar": 1,
        "hutan_primer_sekunder_ke_lahan_lainnya_share": 1,
        "hutan_primer_sekunder": 1,
    },
)
def hutan_primer_hutan_sekunder_ke_lahan_lainnya():
    return (
        availability_effect_hutan_dan_belukar()
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
        "availability_effect_hutan_dan_belukar": 1,
        "hutan_primer_sekunder": 1,
    },
)
def hutan_primer_hutan_sekunder_to_belukar_padang_rumput():
    return (
        hutan_primer_sekunder_to_belukar_padang_rumput_share()
        * availability_effect_hutan_dan_belukar()
        * hutan_primer_sekunder()
    )


@component.add(
    name='"Hutan Primer & Hutan Sekunder to Hutan Mangrove"',
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "availability_effect_hutan_dan_belukar": 1,
        "hutan_primer_sekunder_to_hutan_mangrove_share": 1,
        "hutan_primer_sekunder": 1,
    },
)
def hutan_primer_hutan_sekunder_to_hutan_mangrove():
    return (
        availability_effect_hutan_dan_belukar()
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
        "availability_effect_hutan_dan_belukar": 1,
        "hutan_primer_sekunder": 1,
    },
)
def hutan_primer_hutan_sekunder_to_hutan_tanaman():
    return (
        hutan_primer_sekunder_to_hutan_tanaman_share()
        * availability_effect_hutan_dan_belukar()
        * hutan_primer_sekunder()
    )


@component.add(
    name='"Hutan Primer & Hutan Sekunder to Perkebunan"',
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hutan_primer_sekunder_to_perkebunan_share": 1,
        "availability_effect_hutan_dan_belukar": 1,
        "hutan_primer_sekunder": 1,
    },
)
def hutan_primer_hutan_sekunder_to_perkebunan():
    return (
        hutan_primer_sekunder_to_perkebunan_share()
        * availability_effect_hutan_dan_belukar()
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
        "availability_effect_hutan_dan_belukar": 1,
        "hutan_primer_sekunder": 1,
    },
)
def hutan_primer_hutan_sekunderke_pertambangan():
    return (
        hutan_primer_sekunder_ke_pertambangan_share()
        * availability_effect_hutan_dan_belukar()
        * hutan_primer_sekunder()
    )


@component.add(
    name='"Hutan Primer & Hutan Sekunder ke Rawa & Badan Air"',
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hutan_primer_sekunder_ke_rawa_badan_air_share": 1,
        "availability_effect_hutan_dan_belukar": 1,
        "hutan_primer_sekunder": 1,
    },
)
def hutan_primer_hutan_sekunder_ke_rawa_badan_air():
    return (
        hutan_primer_sekunder_ke_rawa_badan_air_share()
        * availability_effect_hutan_dan_belukar()
        * hutan_primer_sekunder()
    )


@component.add(
    name='"Hutan Primer & Hutan Sekunder to Pertanian"',
    units="Ha/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hutan_primer_sekunder_to_pertanian_share": 1,
        "availability_effect_hutan_dan_belukar": 1,
        "hutan_primer_sekunder": 1,
    },
)
def hutan_primer_hutan_sekunder_to_pertanian():
    return (
        hutan_primer_sekunder_to_pertanian_share()
        * availability_effect_hutan_dan_belukar()
        * hutan_primer_sekunder()
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
        [2016, 2019, 2022, 2025, 2030, 2035, 2040, 2045, 2050, 2055],
        [55752, 66979, 66979, 66979, 66977, 66979, 66979, 66979, 66979, 66979],
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
    name="Time Index",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "time_unit": 1},
)
def time_index():
    return time() / time_unit()


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
    name="Padang Rumput Minimum",
    units="Ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"belukar_padang_rumput_init": 1, "minimum_fraction_padang_rumput": 1},
)
def padang_rumput_minimum():
    return belukar_padang_rumput_init() * minimum_fraction_padang_rumput()


@component.add(
    name="Availability Effect Hutan dan Belukar",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"hutan_dan_belukar_ratio": 1},
)
def availability_effect_hutan_dan_belukar():
    return np.interp(
        hutan_dan_belukar_ratio(),
        [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0],
        [0.0, 0.0, 0.14, 0.255, 0.426, 0.574, 0.71, 0.83, 0.91, 0.97, 1.0],
    )


@component.add(
    name='"Availability Effect Rawa & Badan Air"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"hutan_lindung_konservasi_ratio": 1},
)
def availability_effect_rawa_badan_air():
    return np.interp(
        hutan_lindung_konservasi_ratio(),
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
    depends_on={"padang_rumput_ratio": 1},
)
def availability_effect_belukar_padang_rumput():
    return np.interp(
        padang_rumput_ratio(),
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
    depends_on={"pertanian_lahan_basah_ratio": 1},
)
def availability_effect_hutan_mangrove():
    return np.interp(
        pertanian_lahan_basah_ratio(),
        [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0],
        [0.0, 0.0, 0.14, 0.255, 0.426, 0.574, 0.71, 0.83, 0.91, 0.97, 1.0],
    )


@component.add(
    name="Availability Effect Hutan Tanaman",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"pertanian_lahan_kering_ratio": 1},
)
def availability_effect_hutan_tanaman():
    return np.interp(
        pertanian_lahan_kering_ratio(),
        [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0],
        [0.0, 0.0, 0.14, 0.255, 0.426, 0.574, 0.71, 0.83, 0.91, 0.97, 1.0],
    )


@component.add(
    name="Availability Effect Pertanian",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"tambak_ratio": 1},
)
def availability_effect_pertanian():
    return np.interp(
        tambak_ratio(),
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
    name="Hutan dan Belukar Minimum",
    units="Ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hutan_primer_sekunder_init": 1,
        "minimum_fraction_hutan_dan_belukar": 1,
    },
)
def hutan_dan_belukar_minimum():
    return hutan_primer_sekunder_init() * minimum_fraction_hutan_dan_belukar()


@component.add(
    name="Hutan dan Belukar Ratio",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hutan_primer_sekunder": 1, "hutan_dan_belukar_minimum": 1},
)
def hutan_dan_belukar_ratio():
    return hutan_primer_sekunder() / hutan_dan_belukar_minimum()


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
    name="Time Index 0",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "time_unit": 1},
)
def time_index_0():
    return time() / time_unit()


@component.add(
    name='"Hutan Lindung & Konservasi Minimum"',
    units="Ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "rawa_badan_air_init": 1,
        "minimum_fraction_hutan_lindung_konservasi": 1,
    },
)
def hutan_lindung_konservasi_minimum():
    return rawa_badan_air_init() * minimum_fraction_hutan_lindung_konservasi()


@component.add(
    name='"Hutan Lindung & Konservasi Ratio"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"rawa_badan_air": 1, "hutan_lindung_konservasi_minimum": 1},
)
def hutan_lindung_konservasi_ratio():
    return rawa_badan_air() / hutan_lindung_konservasi_minimum()


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
    name="Minimum Fraction Padang Rumput",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index_0": 1},
)
def minimum_fraction_padang_rumput():
    return np.interp(
        time_index_0(),
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
    depends_on={"time_index_0": 1},
)
def minimum_fraction_pertambangan():
    return np.interp(
        time_index_0(),
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
    name="Minimum Fraction Pertanian Lahan Kering",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index_0": 1},
)
def minimum_fraction_pertanian_lahan_kering():
    return np.interp(
        time_index_0(),
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
    name="Minimum Fraction Tambak",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index_0": 1},
)
def minimum_fraction_tambak():
    return np.interp(
        time_index_0(),
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
    name="Padang Rumput Ratio",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"belukar_padang_rumput": 1, "padang_rumput_minimum": 1},
)
def padang_rumput_ratio():
    return belukar_padang_rumput() / padang_rumput_minimum()


@component.add(
    name="Pertanian Lahan Kering Minimum",
    units="Ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hutan_tanaman_init": 1, "minimum_fraction_pertanian_lahan_kering": 1},
)
def pertanian_lahan_kering_minimum():
    return hutan_tanaman_init() * minimum_fraction_pertanian_lahan_kering()


@component.add(
    name="Pertanian Lahan Kering Ratio",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hutan_tanaman": 1, "pertanian_lahan_kering_minimum": 1},
)
def pertanian_lahan_kering_ratio():
    return hutan_tanaman() / pertanian_lahan_kering_minimum()


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
    name="Minimum Fraction Hutan dan Belukar",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index_0": 1},
)
def minimum_fraction_hutan_dan_belukar():
    return np.interp(
        time_index_0(),
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
    name='"Minimum Fraction Hutan Lindung & Konservasi"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index_0": 1},
)
def minimum_fraction_hutan_lindung_konservasi():
    return np.interp(
        time_index_0(),
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
    depends_on={"time_index_0": 1},
)
def minimum_fraction_perkebunan():
    return np.interp(
        time_index_0(),
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
    name="Tambak Minimum",
    units="Ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pertanian_init": 1, "minimum_fraction_tambak": 1},
)
def tambak_minimum():
    return pertanian_init() * minimum_fraction_tambak()


@component.add(
    name="Minimum Fraction Lahan Terbangun",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index_0": 1},
)
def minimum_fraction_lahan_terbangun():
    return np.interp(
        time_index_0(),
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
    name="Minimum Fraction Pertanian Lahan Basah",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index_0": 1},
)
def minimum_fraction_pertanian_lahan_basah():
    return np.interp(
        time_index_0(),
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
    name="Pertanian Lahan Basah Minimum",
    units="Ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hutan_mangrove_init": 1, "minimum_fraction_pertanian_lahan_basah": 1},
)
def pertanian_lahan_basah_minimum():
    return hutan_mangrove_init() * minimum_fraction_pertanian_lahan_basah()


@component.add(
    name="Pertanian Lahan Basah Ratio",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hutan_mangrove": 1, "pertanian_lahan_basah_minimum": 1},
)
def pertanian_lahan_basah_ratio():
    return hutan_mangrove() / pertanian_lahan_basah_minimum()


@component.add(
    name="Tambak Ratio",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pertanian": 1, "tambak_minimum": 1},
)
def tambak_ratio():
    return pertanian() / tambak_minimum()


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
    depends_on={"time_index_0": 1},
)
def minimum_fraction_lahan_lainnya():
    return np.interp(
        time_index_0(),
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
    name="Belukar Padang Rumput Hist",
    units="Ha",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_index": 1},
)
def belukar_padang_rumput_hist():
    return np.interp(
        time_index(),
        [
            2016.0,
            2019.0,
            2022.0,
            2025.0,
            2030.0,
            2035.0,
            2040.0,
            2045.0,
            2050.0,
            2055.0,
        ],
        [
            1649370.0,
            1762750.0,
            1832730.0,
            1838880.0,
            1798060.0,
            1774720.0,
            1707740.0,
            1653230.0,
            1602890.0,
            1563240.0,
        ],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            5.60000e-04,
            5.40000e-04,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            1.68433e-07,
            1.69533e-07,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
        ],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            2.56500e-03,
            2.48000e-03,
            2.51100e-03,
            2.46200e-03,
            3.44000e-04,
            3.44000e-04,
            4.38000e-04,
            4.43000e-04,
            4.28000e-04,
            4.31000e-04,
            2.39000e-04,
            2.44000e-04,
            1.28000e-04,
            1.31000e-04,
            5.90627e-05,
            5.99759e-05,
            1.86692e-05,
            1.89030e-05,
            1.91427e-05,
        ],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            3.04302e-07,
            2.94191e-07,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
        ],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            0.0358,
            0.0346,
            0.028,
            0.0275,
            0.0247,
            0.0246,
            0.0137,
            0.0139,
            0.0084,
            0.0085,
            0.0066,
            0.0067,
            0.0022,
            0.0022,
            0.0028,
            0.0029,
            0.0019,
            0.0019,
            0.0019,
        ],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            0.0036,
            0.0035,
            0.0036,
            0.0035,
            0.0056,
            0.0056,
            0.0054,
            0.0054,
            0.0038,
            0.0038,
            0.0036,
            0.0037,
            0.003,
            0.0031,
            0.0026,
            0.0026,
            0.0036,
            0.0036,
            0.0037,
        ],
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
        [
            2016,
            2018,
            2019,
            2021,
            2022,
            2024,
            2025,
            2029,
            2030,
            2034,
            2035,
            2039,
            2040,
            2044,
            2045,
            2049,
            2050,
            2054,
            2055,
        ],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            0.00021,
            0.0002,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            0.000864,
            0.000836,
            0.000697,
            0.000684,
            0.000381,
            0.00038,
            0.000694,
            0.000702,
            0.000691,
            0.000695,
            0.000606,
            0.000618,
            0.000463,
            0.000471,
            0.000283,
            0.000288,
            0.000194,
            0.000196,
            0.000199,
        ],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            0.0274,
            0.0265,
            0.0269,
            0.0263,
            0.0426,
            0.0425,
            0.0297,
            0.0301,
            0.0166,
            0.0167,
            0.0092,
            0.0094,
            0.006,
            0.0061,
            0.0059,
            0.006,
            0.0056,
            0.0057,
            0.0058,
        ],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            0.00193,
            0.00196,
            0.00169,
            0.00171,
            0.00411,
            0.00419,
            0.0053,
            0.00545,
            0.00783,
            0.00814,
            0.00591,
            0.00604,
            0.00337,
            0.00343,
            0.00284,
            0.00288,
            0.00241,
            0.00244,
            0.00248,
        ],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            0.029,
            0.029,
            0.027,
            0.027,
            0.028,
            0.028,
            0.016,
            0.016,
            0.012,
            0.013,
            0.007,
            0.007,
            0.003,
            0.003,
            0.003,
            0.003,
            0.004,
            0.004,
            0.004,
        ],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            1.12622e-06,
            1.14494e-06,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
        ],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            3.38509e-05,
            3.44136e-05,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
        ],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            6.51111e-04,
            6.61935e-04,
            5.15291e-04,
            5.21882e-04,
            4.99511e-04,
            5.09494e-04,
            1.55476e-04,
            1.59884e-04,
            7.88817e-05,
            8.20127e-05,
            5.03824e-05,
            5.15196e-05,
            5.46350e-05,
            5.55218e-05,
            5.93537e-05,
            6.01549e-05,
            6.30413e-05,
            6.40123e-05,
            6.50138e-05,
        ],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            0.0214,
            0.0218,
            0.0188,
            0.0191,
            0.0022,
            0.0023,
            0.0029,
            0.003,
            0.0031,
            0.0032,
            0.0025,
            0.0025,
            0.002,
            0.002,
            0.0018,
            0.0018,
            0.0015,
            0.0015,
            0.0016,
        ],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            0.00152,
            0.00138,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            0.00111,
            0.001,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            1.41000e-03,
            1.28000e-03,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            4.52162e-06,
            4.52168e-06,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
        ],
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
        [2016, 2019, 2022, 2025, 2030, 2035, 2040, 2045, 2050, 2055],
        [2473, 3865, 3865, 3865, 3865, 3865, 3865, 3865, 3865, 3865],
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
        [
            2016,
            2018,
            2019,
            2021,
            2022,
            2024,
            2025,
            2029,
            2030,
            2034,
            2035,
            2039,
            2040,
            2044,
            2045,
            2049,
            2050,
            2054,
            2055,
        ],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
        [
            2016,
            2018,
            2019,
            2021,
            2022,
            2024,
            2025,
            2029,
            2030,
            2034,
            2035,
            2039,
            2040,
            2044,
            2045,
            2049,
            2050,
            2054,
            2055,
        ],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
        time_index(),
        [
            2016,
            2018,
            2019,
            2021,
            2022,
            2024,
            2025,
            2029,
            2030,
            2034,
            2035,
            2039,
            2040,
            2044,
            2045,
            2049,
            2050,
            2054,
            2055,
        ],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
        [
            2016,
            2018,
            2019,
            2021,
            2022,
            2024,
            2025,
            2029,
            2030,
            2034,
            2035,
            2039,
            2040,
            2044,
            2045,
            2049,
            2050,
            2054,
            2055,
        ],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            0.0084,
            0.0065,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            0.003,
            0.0024,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
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
        [
            2016,
            2018,
            2019,
            2021,
            2022,
            2024,
            2025,
            2029,
            2030,
            2034,
            2035,
            2039,
            2040,
            2044,
            2045,
            2049,
            2050,
            2054,
            2055,
        ],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
        time_index(),
        [
            2016,
            2018,
            2019,
            2021,
            2022,
            2024,
            2025,
            2029,
            2030,
            2034,
            2035,
            2039,
            2040,
            2044,
            2045,
            2049,
            2050,
            2054,
            2055,
        ],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            0.02,
            0.016,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
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
        [2016, 2019, 2022, 2025, 2030, 2035, 2040, 2045, 2050, 2055],
        [1665, 3250, 3250, 3250, 3250, 3250, 3250, 3250, 3250, 3250],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            0.0045,
            0.0031,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
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
        [
            2016,
            2018,
            2019,
            2021,
            2022,
            2024,
            2025,
            2029,
            2030,
            2034,
            2035,
            2039,
            2040,
            2044,
            2045,
            2049,
            2050,
            2054,
            2055,
        ],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
        [
            2016,
            2018,
            2019,
            2021,
            2022,
            2024,
            2025,
            2029,
            2030,
            2034,
            2035,
            2039,
            2040,
            2044,
            2045,
            2049,
            2050,
            2054,
            2055,
        ],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
        [
            2016,
            2018,
            2019,
            2021,
            2022,
            2024,
            2025,
            2029,
            2030,
            2034,
            2035,
            2039,
            2040,
            2044,
            2045,
            2049,
            2050,
            2054,
            2055,
        ],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            0.00056,
            0.00057,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            9.92411e-06,
            1.00891e-05,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
        ],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            3.46145e-04,
            3.51899e-04,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            6.34743e-05,
            6.44520e-05,
            6.54603e-05,
        ],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            0.00481,
            0.00495,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0377,
            0.0413,
            0.0522,
            0.0573,
            0.0402,
            0.0436,
            0.0353,
            0.0376,
            0.0487,
            0.0511,
            0.0538,
        ],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            2.80000e-04,
            2.90000e-04,
            0.00000e00,
            0.00000e00,
            1.63000e-04,
            1.66000e-04,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            1.10425e-05,
            1.10335e-05,
            4.28183e-05,
            4.27309e-05,
            5.47629e-05,
            5.46229e-05,
            5.44837e-05,
        ],
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
        [
            2016,
            2018,
            2019,
            2021,
            2022,
            2024,
            2025,
            2029,
            2030,
            2034,
            2035,
            2039,
            2040,
            2044,
            2045,
            2049,
            2050,
            2054,
            2055,
        ],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
        [
            2016.0,
            2019.0,
            2022.0,
            2025.0,
            2030.0,
            2035.0,
            2040.0,
            2045.0,
            2050.0,
            2055.0,
        ],
        [
            167930.0,
            279301.0,
            394528.0,
            543679.0,
            769866.0,
            991880.0,
            1159230.0,
            1277600.0,
            1373320.0,
            1461290.0,
        ],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            0.00046,
            0.00035,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            0.000189,
            0.000142,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            0.000183,
            0.000138,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
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
        [
            2016,
            2018,
            2019,
            2021,
            2022,
            2024,
            2025,
            2029,
            2030,
            2034,
            2035,
            2039,
            2040,
            2044,
            2045,
            2049,
            2050,
            2054,
            2055,
        ],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
        [
            2016,
            2018,
            2019,
            2021,
            2022,
            2024,
            2025,
            2029,
            2030,
            2034,
            2035,
            2039,
            2040,
            2044,
            2045,
            2049,
            2050,
            2054,
            2055,
        ],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            0.00601,
            0.00546,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
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
        time_index(),
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            5.0e-05,
            4.0e-05,
            0.0e00,
            0.0e00,
            0.0e00,
            0.0e00,
            0.0e00,
            0.0e00,
            0.0e00,
            0.0e00,
            0.0e00,
            0.0e00,
            0.0e00,
            0.0e00,
            0.0e00,
            0.0e00,
            0.0e00,
            0.0e00,
            0.0e00,
        ],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            0.0093,
            0.0085,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            0.00051,
            0.00047,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
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
        [
            2016.0,
            2019.0,
            2022.0,
            2025.0,
            2030.0,
            2035.0,
            2040.0,
            2045.0,
            2050.0,
            2055.0,
        ],
        [
            2696440.0,
            2608260.0,
            2542390.0,
            2442760.0,
            2308080.0,
            2131850.0,
            2037740.0,
            1972640.0,
            1920100.0,
            1861840.0,
        ],
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
        time_index(),
        [
            2016,
            2018,
            2019,
            2021,
            2022,
            2024,
            2025,
            2029,
            2030,
            2034,
            2035,
            2039,
            2040,
            2044,
            2045,
            2049,
            2050,
            2054,
            2055,
        ],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            0.00133,
            0.00079,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.000623,
            0.000629,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            0.0021,
            0.0012,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            0.022,
            0.0131,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0055,
            0.00529,
            0.00049,
            0.00049,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
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
        time_index(),
        [
            2016,
            2018,
            2019,
            2021,
            2022,
            2024,
            2025,
            2029,
            2030,
            2034,
            2035,
            2039,
            2040,
            2044,
            2045,
            2049,
            2050,
            2054,
            2055,
        ],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
        time_index(),
        [
            2016,
            2018,
            2019,
            2021,
            2022,
            2024,
            2025,
            2029,
            2030,
            2034,
            2035,
            2039,
            2040,
            2044,
            2045,
            2049,
            2050,
            2054,
            2055,
        ],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            0.07,
            0.042,
            0.0,
            0.0,
            0.047,
            0.044,
            0.037,
            0.036,
            0.047,
            0.047,
            0.043,
            0.044,
            0.035,
            0.035,
            0.026,
            0.026,
            0.021,
            0.021,
            0.021,
        ],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            0.00678,
            0.00697,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            0.0078,
            0.008,
            0.205,
            0.299,
            0.189,
            0.167,
            0.194,
            0.2,
            0.16,
            0.175,
            0.112,
            0.123,
            0.0629,
            0.0681,
            0.0189,
            0.0201,
            0.0,
            0.0,
            0.0,
        ],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            0.00262,
            0.00269,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            0.1385,
            0.1425,
            0.1274,
            0.1855,
            0.0108,
            0.0095,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
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
        [
            2016,
            2018,
            2019,
            2021,
            2022,
            2024,
            2025,
            2029,
            2030,
            2034,
            2035,
            2039,
            2040,
            2044,
            2045,
            2049,
            2050,
            2054,
            2055,
        ],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            0.00918,
            0.00944,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            0.00226,
            0.00232,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            0.00078,
            0.0008,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
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
        time_index(),
        [
            2016,
            2018,
            2019,
            2021,
            2022,
            2024,
            2025,
            2029,
            2030,
            2034,
            2035,
            2039,
            2040,
            2044,
            2045,
            2049,
            2050,
            2054,
            2055,
        ],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
        [
            2016,
            2018,
            2019,
            2021,
            2022,
            2024,
            2025,
            2029,
            2030,
            2034,
            2035,
            2039,
            2040,
            2044,
            2045,
            2049,
            2050,
            2054,
            2055,
        ],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
        time_index(),
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            0.023,
            0.015,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            0.000182,
            0.000188,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            8.34032e-05,
            6.26337e-05,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
        ],
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
        [2016, 2019, 2022, 2025, 2030, 2035, 2040, 2045, 2050, 2055],
        [38687, 35674, 35674, 35674, 35674, 35674, 35674, 35674, 35674, 35674],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            0.012,
            0.012,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            0.0042,
            0.0044,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
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
        [
            2016,
            2018,
            2019,
            2021,
            2022,
            2024,
            2025,
            2029,
            2030,
            2034,
            2035,
            2039,
            2040,
            2044,
            2045,
            2049,
            2050,
            2054,
            2055,
        ],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            0.0009,
            0.000676,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            0.0047,
            0.0035,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            0.000209,
            0.000216,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            7.82650e-05,
            5.87751e-05,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
        ],
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
        time_index(),
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            2.11276e-05,
            1.58663e-05,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
        ],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            0.018,
            0.014,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
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
        [2016, 2019, 2022, 2025, 2030, 2035, 2040, 2045, 2050, 2055],
        [7215, 16997, 24717, 28231, 30490, 30360, 29696, 29106, 28736, 28509],
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
        time_index(),
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            0.000698,
            0.000416,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
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
        [
            2016,
            2018,
            2019,
            2021,
            2022,
            2024,
            2025,
            2029,
            2030,
            2034,
            2035,
            2039,
            2040,
            2044,
            2045,
            2049,
            2050,
            2054,
            2055,
        ],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
        [
            2016.0,
            2019.0,
            2022.0,
            2025.0,
            2030.0,
            2035.0,
            2040.0,
            2045.0,
            2050.0,
            2055.0,
        ],
        [
            2513660.0,
            2358250.0,
            2253560.0,
            2190760.0,
            2138840.0,
            2119340.0,
            2116060.0,
            2119530.0,
            2128200.0,
            2139110.0,
        ],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            0.000653,
            0.000674,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            1.73000e-04,
            1.79000e-04,
            0.00000e00,
            0.00000e00,
            1.43700e-03,
            1.45800e-03,
            1.04100e-03,
            1.05400e-03,
            8.49000e-04,
            8.52000e-04,
            6.00000e-04,
            6.00000e-04,
            2.67000e-04,
            2.66000e-04,
            8.12756e-05,
            8.11097e-05,
            4.14776e-05,
            4.13716e-05,
            4.12661e-05,
        ],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            6.75275e-05,
            6.96815e-05,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
            0.00000e00,
        ],
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
        [2016, 2019, 2022, 2025, 2030, 2035, 2040, 2045, 2050, 2055],
        [37831, 35700, 13345, 16950, 15926, 13112, 10796, 9147, 8019, 7266],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            0.0006,
            0.00041,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            0.0279,
            0.0288,
            0.0246,
            0.0252,
            0.0296,
            0.03,
            0.0208,
            0.0211,
            0.0096,
            0.0096,
            0.0037,
            0.0037,
            0.0011,
            0.0011,
            0.0012,
            0.0012,
            0.0014,
            0.0014,
            0.0014,
        ],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            0.005,
            0.0052,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            0.0012,
            0.0012,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            0.028,
            0.03,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            0.0221,
            0.0228,
            0.01932,
            0.01975,
            0.0029,
            0.00294,
            0.00134,
            0.00135,
            0.00047,
            0.00047,
            0.00034,
            0.00034,
            0.00019,
            0.00019,
            0.00019,
            0.00019,
            0.00018,
            0.00018,
            0.00018,
        ],
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
        time_index(),
        [
            2016,
            2018,
            2019,
            2021,
            2022,
            2024,
            2025,
            2029,
            2030,
            2034,
            2035,
            2039,
            2040,
            2044,
            2045,
            2049,
            2050,
            2054,
            2055,
        ],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            0.0119,
            0.0123,
            0.0117,
            0.012,
            0.0128,
            0.013,
            0.0102,
            0.0103,
            0.0091,
            0.0092,
            0.0068,
            0.0068,
            0.0055,
            0.0055,
            0.0044,
            0.0044,
            0.0034,
            0.0034,
            0.0034,
        ],
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
        time_index(),
        [
            2016,
            2018,
            2019,
            2021,
            2022,
            2024,
            2025,
            2029,
            2030,
            2034,
            2035,
            2039,
            2040,
            2044,
            2045,
            2049,
            2050,
            2054,
            2055,
        ],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
        [
            2016.0,
            2018.0,
            2019.0,
            2021.0,
            2022.0,
            2024.0,
            2025.0,
            2029.0,
            2030.0,
            2034.0,
            2035.0,
            2039.0,
            2040.0,
            2044.0,
            2045.0,
            2049.0,
            2050.0,
            2054.0,
            2055.0,
        ],
        [
            0.0099,
            0.0103,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
    )


@component.add(
    name="IKU Bali nusra",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_iku_bali_nusra": 1},
    other_deps={
        "_integ_iku_bali_nusra": {"initial": {}, "step": {"perubahan_iku_bali": 1}}
    },
)
def iku_bali_nusra():
    """
    Interpolasi ke 2010
    """
    return _integ_iku_bali_nusra()


_integ_iku_bali_nusra = Integ(
    lambda: perubahan_iku_bali(), lambda: 94.7, "_integ_iku_bali_nusra"
)


@component.add(
    name="IKU Bali nusra Historis",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def iku_bali_nusra_historis():
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
        "iku_bali_nusra": 1,
        "elastisitas_perubahan_iku_bali_nusra": 1,
        "laju_pdrb_per_kapita": 1,
    },
)
def perubahan_iku_bali():
    return (
        iku_bali_nusra()
        * elastisitas_perubahan_iku_bali_nusra()
        * laju_pdrb_per_kapita()
    )


@component.add(
    name="Lahan Pangan per kapita",
    units="Ha/jiwa",
    comp_type="Constant",
    comp_subtype="Normal",
)
def lahan_pangan_per_kapita():
    """
    hitungan matra lahan, 2023
    """
    return 0.0754683


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
    name="Elastisitas perubahan IKU Bali nusra",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def elastisitas_perubahan_iku_bali_nusra():
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
        [0.092893, 0.094337, 0.111783, 0.113434, 0.11, 0.2],
    )


@component.add(
    name='"debit per detik pertanian dasar SK 146/2023"',
    units="m*m*m/detik/Ha",
    comp_type="Constant",
    comp_subtype="Normal",
)
def debit_per_detik_pertanian_dasar_sk_1462023():
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
    lambda: 0.025,
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
    return 16324100000.0


@component.add(
    name='"std kebutuhan air per pertanian dasar SK 146/2023 tahunan"',
    units="m*m*m/(tahun*Ha)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "konverter_detik_ke_jam": 1,
        "konverter_jam_ke_hari": 1,
        "jumlah_hari_per_musim_tanam": 1,
        "intensitas_penanaman": 1,
        "debit_per_detik_pertanian_dasar_sk_1462023": 1,
    },
)
def std_kebutuhan_air_per_pertanian_dasar_sk_1462023_tahunan():
    return (
        konverter_detik_ke_jam()
        * konverter_jam_ke_hari()
        * jumlah_hari_per_musim_tanam()
        / intensitas_penanaman()
        * debit_per_detik_pertanian_dasar_sk_1462023()
    )


@component.add(
    name="Potensi air tanah",
    units="m*m*m/tahun",
    comp_type="Constant",
    comp_subtype="Normal",
)
def potensi_air_tanah():
    return 11526000000.0


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
    name="PDRB Pulau",
    units="JutaRp/tahun",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pdrb_pulau_awal": 1,
        "kapital_awal": 1,
        "kapital": 1,
        "intensitas_kapital": 2,
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
            6630610.0,
            6451910.0,
            6547460.0,
            6553620.0,
            6786010.0,
            6935630.0,
            7281020.0,
            7229230.0,
            7485180.0,
            7557550.0,
            8105140.0,
            8238960.0,
            8560140.0,
            8657180.0,
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
            2010.0,
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
        [1.0, 0.995, 0.95, 0.96, 0.85, 0.84, 0.84, 0.835, 0.85, 0.9, 1.0],
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
        time(), [2010.0, 2024.0, 2025.0, 2026.0, 2030.0], [0.35, 0.35, 0.35, 0.35, 0.35]
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
    return 0.5


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
            6.21634e07,
            6.80665e07,
            7.41682e07,
            7.79402e07,
            8.39464e07,
            9.18455e07,
            1.01482e08,
            1.05677e08,
            1.13119e08,
            1.18713e08,
            1.07975e08,
            1.08611e08,
            1.08986e08,
            1.15208e08,
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
    depends_on={"laju_pertumbuhan_populasi_table": 1, "time": 1, "satu_tahun_unit": 1},
)

def laju_pertumbuhan_populasi():
    current_time = time() / satu_tahun_unit()
    return laju_pertumbuhan_populasi_table(current_time)


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
        0.0223306,
        0.005703,
        0.0129645,
        0.0201621,
        0.0138583,
        0.013562,
        0.0132592,
        0.0129768,
        0.0126781,
        0.0198591,
        -0.00139049,
        0.014386,
        0.0116116,
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
    name="Lpe Provinsi historis",
    units="Dmnl/tahun",
    comp_type="Stateful",
    comp_subtype="Trend",
    depends_on={"_trend_lpe_provinsi_historis": 1},
    other_deps={
        "_trend_lpe_provinsi_historis": {
            "initial": {
                "lpe_pulau_mulamula": 1,
                "pdrb_pulau_historis": 1,
                "waktu_trend_lpe_pulau": 1,
            },
            "step": {"pdrb_pulau_historis": 1, "waktu_trend_lpe_pulau": 1},
        }
    },
)
def lpe_provinsi_historis():
    return _trend_lpe_provinsi_historis()


_trend_lpe_provinsi_historis = Trend(
    lambda: pdrb_pulau_historis(),
    lambda: waktu_trend_lpe_pulau(),
    lambda: lpe_pulau_mulamula(),
    "_trend_lpe_provinsi_historis",
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
            2024.0,
        ],
        [
            0.3,
            0.35,
            0.37,
            0.37,
            0.36,
            0.37,
            0.35,
            0.36,
            0.38,
            0.39,
            0.34,
            0.35,
            0.35,
            0.36,
            0.36,
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
            2.07719e08,
            2.13705e08,
            2.22155e08,
            2.35375e08,
            2.49269e08,
            2.75235e08,
            2.91499e08,
            3.02267e08,
            3.10351e08,
            3.25955e08,
            3.09597e08,
            3.09850e08,
            3.25599e08,
            3.38611e08,
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
            13097200.0,
            13389600.0,
            13466000.0,
            13640600.0,
            13915600.0,
            14108400.0,
            14299800.0,
            14489400.0,
            14677400.0,
            14863500.0,
            15158700.0,
            15137600.0,
            15355400.0,
            15533700.0,
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
            6371520.0,
            6217660.0,
            6326920.0,
            6328420.0,
            6540960.0,
            6671600.0,
            7060930.0,
            7035090.0,
            7291360.0,
            7385790.0,
            7725330.0,
            7907870.0,
            8240710.0,
            8407700.0,
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
        0.577,
        0.549,
        0.574,
        0.563,
        0.564,
        0.571,
        0.586,
        0.573,
        0.597,
        0.578,
        0.595,
        0.591,
        0.62,
        0.611,
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
