from options import Options
from chart import Chart, Place, Time
import planets
import wx
import util
import math
import astrology
import chart, houses, planets, fortune
import fixstars
import options
import common
import util
import mtexts
import datetime

def main():
    options = Options()

    location = Place(
        place=u'',
        deglon=142,
        minlon=44,
        seclon=0,
        east=True,
        deglat=46,
        minlat=57,
        seclat=0,
        north=True,
        altitude=100
    )

    birth_time = Time(
        day=3,
        month=12,
        year=1997,
        hour=13,
        minute=55,
        second=0,
        bc=False,
        cal=0,
        zt=0,
        plus=True,
        zh=10,
        place=location,
        zm=0,
        daylightsaving=False
    )

    name = u'Olya'
    male = False
    htype = 0
    notes = u''
    options = Options()
    full = True
    proftype = 0
    nolat = False

    birth_chart = Chart(
        name=name,
        male=male,
        time=birth_time,
        place=location,
        htype=htype,
        notes=notes,
        options=options,
        full=full,
        proftype=proftype,
        nolat=nolat
    )

    current_time = Time(
        day=03,
        month=12,
        year=2023,
        hour=datetime.datetime.now().hour,
        minute=datetime.datetime.now().minute,
        second=datetime.datetime.now().second,
        bc=False,
        cal=0,
        zt=0,
        plus=True,
        zh=11,
        place=location,
        zm=0,
        daylightsaving=False
    )
    current_chart = Chart(
        name="Current",
        male=male,
        time=current_time,
        place=location,
        htype=htype,
        notes=notes,
        options=options,
        full=full,
        proftype=proftype,
        nolat=nolat
    )

    compareCharts(birth_chart, current_chart, options)


def drawAspectSymbols(chart, options):
    for i in range(planets.Planets.PLANETS_NUM - 1):
        if (i == astrology.SE_URANUS and not options.transcendental[chart.TRANSURANUS]) or (
                i == astrology.SE_NEPTUNE and not options.transcendental[chart.TRANSNEPTUNE]) or (
                i == astrology.SE_PLUTO and not options.transcendental[chart.TRANSPLUTO]) or (
                (i == astrology.SE_MEAN_NODE or i == astrology.SE_TRUE_NODE) and not options.shownodes):
            continue
        for j in range(planets.Planets.PLANETS_NUM - 1):
            if (j == astrology.SE_URANUS and not options.transcendental[chart.TRANSURANUS]) or (
                    j == astrology.SE_NEPTUNE and not options.transcendental[chart.TRANSNEPTUNE]) or (
                    j == astrology.SE_PLUTO and not options.transcendental[chart.TRANSPLUTO]) or (
                    (j == astrology.SE_MEAN_NODE or j == astrology.SE_TRUE_NODE) and not options.shownodes):
                continue
            asp = chart.aspmatrix[j][i]
            #print asp.typ
            #print asp
            lon1 = chart.planets.planets[i].data[planets.Planet.LONG]
            lon2 = chart.planets.planets[j].data[planets.Planet.LONG]
            showasp = isShowAsp(asp.typ, lon1, lon2, options, chart)
            if showasp:
                aspect_names = {
                    chart.CONJUNCTIO: 'Conjunction',
                    chart.SEXTIL: 'Sextile',
                    chart.QUADRAT: 'Square',
                    chart.TRIGON: 'Trine',
                    chart.OPPOSITIO: 'Opposition',
                }
                if chart.planets.planets[j].name != "mean Node" and chart.planets.planets[i].name != "mean Node":
                    print("------------------------------------------------------------------------------")
                    print('{} {} {}'.format(chart.planets.planets[i].name, aspect_names[asp.typ],
                                            chart.planets.planets[j].name))


def calculateTransits(birth_chart, current_chart, options):
    for i in range(planets.Planets.PLANETS_NUM - 1):
        for j in range(planets.Planets.PLANETS_NUM - 1):
            birth_asp = birth_chart.aspmatrix[j][i]
            current_asp = current_chart.aspmatrix[j][i]

            birth_lon = birth_chart.planets.planets[i].data[planets.Planet.LONG]
            current_lon = current_chart.planets.planets[j].data[planets.Planet.LONG]

            showasp = isShowAsp(current_asp.typ, birth_lon, current_lon, options, current_chart)

            if showasp:
                aspect_names = {
                    birth_chart.CONJUNCTIO: 'Conjunction',
                    birth_chart.SEXTIL: 'Sextile',
                    birth_chart.QUADRAT: 'Square',
                    birth_chart.TRIGON: 'Trine',
                    birth_chart.OPPOSITIO: 'Opposition',
                }
                if current_chart.planets.planets[j].name != "mean Node" and birth_chart.planets.planets[i].name != "mean Node":
                    print("------------------------------------------------------------------------------")
                    print('{} {} {}'.format(birth_chart.planets.planets[i].name, aspect_names[current_asp.typ],
                                            current_chart.planets.planets[j].name))
def compareCharts(birth_chart, current_chart, options):
    print("Transits:")
    calculateTransits(birth_chart, current_chart, options)


def isShowAsp(typ, lon1, lon2, options, chart):
    res = False

    if typ != Chart.NONE and options.aspect[typ]:
        val = True
        if options.traditionalaspects:
            if not(typ == Chart.CONJUNCTIO or typ == Chart.SEXTIL or typ == Chart.QUADRAT or typ == Chart.TRIGON or typ == Chart.OPPOSITIO):
                val = False
            else:
                lona1 = lon1
                lona2 = lon2
                if options.ayanamsha != 0:
                    lona1 -= chart.ayanamsha
                    lona1 = util.normalize(lona1)
                    lona2 -= chart.ayanamsha
                    lona2 = util.normalize(lona2)

                sign1 = int(lona1/Chart.SIGN_DEG)
                sign2 = int(lona2/Chart.SIGN_DEG)
                signdiff = math.fabs(sign1-sign2)
                if signdiff > Chart.SIGN_NUM/2:
                    signdiff = Chart.SIGN_NUM-signdiff
                if options.arsigndiff[typ] != signdiff:
                    val = False

        res = val

    return res

if __name__ == "__main__":
    main()
