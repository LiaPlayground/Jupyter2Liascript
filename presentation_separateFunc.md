<!--

author:  Sebastian Zug, Andre Dietrich

import: https://raw.githubusercontent.com/liaTemplates/PyScript/main/README.md

persistent: true

@path
``` python @PyScript.env
- paths:
  - @0
```
@end

value_input: <span style="display: inline-block; min-width: 9rem">@1:</span> <script 
                input="range"
                output="@0"
                value=@2
                input-always-active
                min="@3"
                max="@4"
                step="0.1"
                modify="false"
            >
            const elements = document.getElementsByClassName("inert");

            for (let i = 0; i < elements.length; i++) {
                elements[i].setAttribute("inert", "");
            }

            setTimeout(() => {
                for (let i = 0; i < elements.length; i++) {
                    elements[i].removeAttribute("inert");
                }
            }, 500);

            @input
            </script>

@python_evaluate
<script class="inert" style="display: block" modify="false" run-once>
`LIASCRIPT:
\`\`\` python @PyScript.repl
@0
\`\`\`
`
</script>
@end

@python_run
<script class="inert" style="display: block" modify="false" run-once>
`LIASCRIPT:
\`\`\` python @Pyodide.exec
@0
\`\`\`
`
</script>
@end
-->

[![LiaScript](https://raw.githubusercontent.com/LiaScript/LiaScript/master/badges/course.svg)]([https://liascript.github.io/course/?](https://liascript.github.io/course/?https://raw.githubusercontent.com/LiaPlayground/Jupyter2Liascript/refs/heads/main/presentation_separateFunc.md#1))


# Beschreibung von Kornverteilungskurven


Im Zuge der Bestimmung einer Sieblinie werden Siebrückstände $m_i$ ermittelt. Die einzelnen zu den Siebdurchmessern $d_i$ gehörigen Siebrückstände $m_i$ können nun auf die Gesamtmasse $m_\text{d} = \sum m_i$ (Annahme vernachlässigbarer Siebverluste) bezogen werden, womit die Masseanteile

$$
    x_i = \frac{m_i}{m_\text{d}}
$$

ermittelt werden. Diese werden typischerweise in einer Summenkurve

$$
    F(d_i) = \sum \limits_{k=1}^i x_i
$$

aufgetragen. Dabei wird aufgrund der über Größenordnungen verteilten Korndurchmesser eine halblogarithmische Darstellung gewählt (siehe folgende Abbildung, rechts). Feinanteile, die nicht durch Siebung näher untersucht werden, sind nicht mit dargestellt. In der linken Abbildung sind die Masseanteile selbst und das zugehörige Histogramm der Masseverteilung dargestellt.

Mithilfe der Körnungslinie bzw. Kornverteilungskurve können die dominierenden Bestandteile (T, U, S, G) ermittelt werden. Des weiteren können die Ungleichförmigkeitszahl

$$
    C_U = \frac{d_{60}}{d_{10}}
$$

und die Krümmungszahl

$$
    C_C = \frac{d_{30}^2}{d_{10}\ d_{60}}
$$

abgeleitet werden. 

> Darauf aufbauend folgt dann ein interaktives Element, in den die Körnungsparameter eingegeben werden können und die Kornverteilungskurve neu berechnet wird.
> 
> ![](notebook.png)


## Variante 1: Interaktive Darstellung ohne Widgets

> Änderungen an den Körnungsparametern sind im Python Code vorzunehmen.

``` python @PyScript.env
- matplotlib
- scipy
- numpy
```

@[path](functions.py)

``` python @PyScript.repl
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import numpy as np
import scipy as sp
from scipy import interpolate
from matplotlib.colors import SymLogNorm
from functions import *

Siebdurchmesser = np.array([63,31.5,16,8,4,2,1,0.5,0.25,0.125,0.063,0.001])
Startwerte = np.array([0,0,842.4,1059.8,1222.9,788.0,706.6,407.6,210.0,195.7,0,0])
plot_KVK_glob(True, Startwerte, Siebdurchmesser)
plt.show()
plt
```

## Variante 2: Interaktive Darstellung mit Widgets und sichtbarem Code

> Für das Triggern der neuen Berechnung und Ausgabe muss nach der Änderung der Werte der grüne Button in der Ecke beider, aufeinander aufbauender Codeblöcke aktiviert werden.

@value_input(a,$63.0\ \text{mm}$,0,-100,200) \
@value_input(b,$31.5\ \text{mm}$,0,-100,200) \
@value_input(c,$16.0\ \text{mm}$,842.4,-100,2000) \
@value_input(d,$ 8.0\ \text{mm}$,1059.8,-100,2000) \
@value_input(e,$ 4.0\ \text{mm}$,1222.9,-100,2000) \
@value_input(f,$ 2.0\ \text{mm}$,788.0,-100,2000) \
@value_input(g,$ 1.0\ \text{mm}$,706.6,-100,2000) \
@value_input(h,$ 0.5\ \text{mm}$,407.6,-100,2000) \
@value_input(i,$ 0.25\ \text{mm}$,210.0,-100,2000) \
@value_input(j,$ 0.125\ \text{mm}$,195.7,-100,2000) \
@value_input(k,$ 0.063\ \text{mm}$,0,-100,200) \
@value_input(l,$ 0.001\ \text{mm}$,0,-100,200)


``` python @python_evaluate
input_values = [@input(`a`), @input(`b`), @input(`c`), @input(`d`), @input(`e`), @input(`f`), @input(`g`), @input(`h`), @input(`i`), @input(`j`), @input(`k`), @input(`l`)]
print(input_values)
```

@[path](functions.py)

``` python @PyScript.repl
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import numpy as np
import scipy as sp
from scipy import interpolate
from matplotlib.colors import SymLogNorm
from functions import *

Siebdurchmesser = np.array([63,31.5,16,8,4,2,1,0.5,0.25,0.125,0.063,0.001])
Startwerte = np.array(input_values)
plot_KVK_glob(True, Startwerte, Siebdurchmesser)
plt.show()
plt
```

## Variante 3: Automatische Weiterleitung von Änderungen an die Darstellung

> Die Darstellung wird automatisch aktualisiert, sobald der Werte geändert wurden.

@value_input(a,$63.0\ \text{mm}$,0,-100,200) \
@value_input(b,$31.5\ \text{mm}$,0,-100,200) \
@value_input(c,$16.0\ \text{mm}$,842.4,-100,2000) \
@value_input(d,$ 8.0\ \text{mm}$,1059.8,-100,2000) \
@value_input(e,$ 4.0\ \text{mm}$,1222.9,-100,2000) \
@value_input(f,$ 2.0\ \text{mm}$,788.0,-100,2000) \
@value_input(g,$ 1.0\ \text{mm}$,706.6,-100,2000) \
@value_input(h,$ 0.5\ \text{mm}$,407.6,-100,2000) \
@value_input(i,$ 0.25\ \text{mm}$,210.0,-100,2000) \
@value_input(j,$ 0.125\ \text{mm}$,195.7,-100,2000) \
@value_input(k,$ 0.063\ \text{mm}$,0,-100,200) \
@value_input(l,$ 0.001\ \text{mm}$,0,-100,200)

@[path](functions.py)

``` python @python_evaluate
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import numpy as np
import scipy as sp
from scipy import interpolate
from matplotlib.colors import SymLogNorm
from functions import *
input_values = [@input(`a`), @input(`b`), @input(`c`), @input(`d`), @input(`e`), @input(`f`), @input(`g`), @input(`h`), @input(`i`), @input(`j`), @input(`k`), @input(`l`)]

Siebdurchmesser = np.array([63,31.5,16,8,4,2,1,0.5,0.25,0.125,0.063,0.001])
Startwerte = np.array(input_values)
plot_KVK_glob(True, Startwerte, Siebdurchmesser)
plt.show()
plt
```


## Variante 4: Hidden Code

> Die Darstellung wird automatisch aktualisiert, sobald der Werte geändert wurden.

@value_input(a,$63.0\ \text{mm}$,0,-100,200) \
@value_input(b,$31.5\ \text{mm}$,0,-100,200) \
@value_input(c,$16.0\ \text{mm}$,842.4,-100,2000) \
@value_input(d,$ 8.0\ \text{mm}$,1059.8,-100,2000) \
@value_input(e,$ 4.0\ \text{mm}$,1222.9,-100,2000) \
@value_input(f,$ 2.0\ \text{mm}$,788.0,-100,2000) \
@value_input(g,$ 1.0\ \text{mm}$,706.6,-100,2000) \
@value_input(h,$ 0.5\ \text{mm}$,407.6,-100,2000) \
@value_input(i,$ 0.25\ \text{mm}$,210.0,-100,2000) \
@value_input(j,$ 0.125\ \text{mm}$,195.7,-100,2000) \
@value_input(k,$ 0.063\ \text{mm}$,0,-100,200) \
@value_input(l,$ 0.001\ \text{mm}$,0,-100,200)

@[path](functions.py)

<script>
`HTML:
<py-script>
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import numpy as np
import scipy as sp
from scipy import interpolate
from matplotlib.colors import SymLogNorm
from functions import *
input_values = [@input(`a`), @input(`b`), @input(`c`), @input(`d`), @input(`e`), @input(`f`), @input(`g`), @input(`h`), @input(`i`), @input(`j`), @input(`k`), @input(`l`)]

Siebdurchmesser = np.array([63,31.5,16,8,4,2,1,0.5,0.25,0.125,0.063,0.001])
Startwerte = np.array(input_values)
plot_KVK_glob(True, Startwerte, Siebdurchmesser)
plt.show()
plt
</py-script>`
</script>

## JavaScript

@value_input(a,$63.0\ \text{mm}$,0,-100,200) \
@value_input(b,$31.5\ \text{mm}$,0,-100,200) \
@value_input(c,$16.0\ \text{mm}$,842.4,-100,2000) \
@value_input(d,$ 8.0\ \text{mm}$,1059.8,-100,2000) \
@value_input(e,$ 4.0\ \text{mm}$,1222.9,-100,2000) \
@value_input(f,$ 2.0\ \text{mm}$,788.0,-100,2000) \
@value_input(g,$ 1.0\ \text{mm}$,706.6,-100,2000) \
@value_input(h,$ 0.5\ \text{mm}$,407.6,-100,2000) \
@value_input(i,$ 0.25\ \text{mm}$,210.0,-100,2000) \
@value_input(j,$ 0.125\ \text{mm}$,195.7,-100,2000) \
@value_input(k,$ 0.063\ \text{mm}$,0,-100,200) \
@value_input(l,$ 0.001\ \text{mm}$,0,-100,200)

<script style="display: block">
// Hilfsfunktionen

// Erzeugt einen Array mit linearen Werten von start bis end in n Schritten.
function linspace(start, end, n) {
  const arr = [];
  const step = (end - start) / (n - 1);
  for (let i = 0; i < n; i++) {
    arr.push(start + step * i);
  }
  return arr;
}

// Findet den Index im Array, dessen Wert am nächsten an "value" liegt.
function findIdxOfNearest(array, value) {
  let minDiff = Infinity;
  let idx = -1;
  array.forEach((d, i) => {
    const diff = Math.abs(d - value);
    if (diff < minDiff) {
      minDiff = diff;
      idx = i;
    }
  });
  return idx;
}

// Erzeugt eine lineare Interpolationsfunktion, die für einen gegebenen x-Wert den interpolierten y-Wert zurückgibt.
// Es wird davon ausgegangen, dass xs aufsteigend sortiert sind.
function linearInterpolator(xs, ys) {
  return function(x) {
    // Falls x außerhalb des Definitionsbereichs liegt
    if (x <= xs[0]) return ys[0];
    if (x >= xs[xs.length - 1]) return ys[ys.length - 1];
    // Suche das Intervall
    let i = 0;
    while (xs[i + 1] < x) {
      i++;
    }
    const t = (x - xs[i]) / (xs[i + 1] - xs[i]);
    return ys[i] + t * (ys[i + 1] - ys[i]);
  };
}

// Berechnet d_n: Für einen gegebenen Anteil (z. B. 10, 30, 60) wird in d_new (im Log‑Raum)
// der Index gesucht, bei dem der interpolierte Wert am nächsten an Anteil liegt.
function d_n(Anteil, d_new, interpFunc) {
  // Erzeuge das Array der interpolierten y-Werte
  const yVals = d_new.map(x => interpFunc(x));
  const idx = findIdxOfNearest(yVals, Anteil);
  return Math.exp(d_new[idx]);
}

// Berechnet die Masseanteile (Relativanteile der Siebmassen).
function masseanteile(siebMassen) {
  const sum = siebMassen.reduce((a, b) => a + b, 0);
  return siebMassen.map(v => v / sum);
}

// Berechnet den Siebdurchgang: Die Massenanteile werden (von hinten) kumulativ aufsummiert,
// wobei das letzte Element weggelassen wird.
function siebdurchgang(massenanteileArr) {
  // Array umkehren
  const rev = massenanteileArr.slice().reverse();
  const cum = [];
  rev.forEach((v, i) => {
    if (i === 0) {
      cum.push(v);
    } else {
      cum.push(cum[i - 1] + v);
    }
  });
  // Letztes Element weglassen und wieder umkehren
  cum.pop();
  return cum.reverse();
}



// Hauptfunktion, die das ECharts‑Objekt erzeugt.
// inputValues: Array mit den Siebmassen (Startwerte)
// siebdurchmesser: Array der Siebdurchmesser (in mm), z. B. [63,31.5,16,8,4,2,1,0.5,0.25,0.125,0.063,0.001]
function plotKVKGlob(inputValues, siebdurchmesser) {
  // 1. Berechnungen analog zum Python-Skript
  const m_i = inputValues;  
  const dm_i = masseanteile(m_i);
  const kumMasseAnteile = siebdurchgang(dm_i); // Länge: siebdurchmesser.length - 1

  // Wir arbeiten nur mit den ersten (n-1) Siebdurchmessern
  const siebPart = siebdurchmesser.slice(0, siebdurchmesser.length - 1);
  // Berechne den Logarithmus der Siebdurchmesser (im Original: np.log)
  const logSieb = siebPart.map(d => Math.log(d));
  
  // Für die Interpolation (wie im Python-Code werden die Arrays "umgedreht")
  const xsInterp = logSieb.slice().reverse(); 
  const ysInterp = kumMasseAnteile.slice().reverse().map(v => v * 100);
  
  // Erstelle die Interpolationsfunktion (hier linear interpoliert)
  const interpFunc = linearInterpolator(xsInterp, ysInterp);
  
  // Erzeuge d_new als linspace im Log‑Raum (hier 1000 Punkte statt 10000 aus Gründen der Performance)
  const d_new = linspace(Math.min(...logSieb), Math.max(...logSieb), 1000);
  
  // Berechne die interpolierten Daten: x = exp(d_new), y = interpFunc(d_new)
  const dataLine = d_new.map(x => [Math.exp(x), interpFunc(x)]);
  
  // Originaldaten (als Punkte)
  const originalData = siebPart.map((d, i) => [d, kumMasseAnteile[i] * 100]);
  
  // Bestimme d10, d30, d60
  const d10 = d_n(10, d_new, interpFunc);
  const d30 = d_n(30, d_new, interpFunc);
  const d60 = d_n(60, d_new, interpFunc);
  
  // Bestimme Gradationsparameter U und Cc sowie entsprechende Klassifizierung
  const U = d60 / d10;
  let U_res = 'ungleichförmig';
  if (U < 5) { U_res = 'gleichförmig'; }
  if (U >= 15) { U_res = 'sehr ungleichförmig'; }
  
  const Cc = (d30 * d30) / (d60 * d10);
  let Cc_res = 'kontinuierlich';
  if (Cc < 1 || Cc > 3) { Cc_res = 'nicht kontinuierlich'; }
  
  if (Cc < 1) {
    if (U < 3) {
      U_res = 'gleichmäßig gestuft';
    } else if (U < 6) {
      U_res = 'eng gestuft';
    } else if (U <= 15) {
      U_res = 'mäßig gestuft';
    }
  } else if (Cc >= 1 && Cc <= 3 && U > 15) {
    U_res = 'weit gestuft';
  } else if (Cc < 0.5 && U > 15) {
    U_res = 'intermittierend gestuft';
  } else {
    U_res = 'Werte';
  }
  
  // 2. Aufbau des ECharts‑Optionsobjekts

  const option = {
    tooltip: {
      trigger: 'axis'
    },
    xAxis: {
        type: 'log',
        name: 'Korndurchmesser d in mm',
        nameLocation: 'middle',  // Positioniert den Achsentitel in der Mitte
        nameGap: 25,             // Abstand zwischen Achse und Titel (anpassbar)
        nameTextStyle: { fontSize: 18 },
        min: 0.001,
        max: 200,
        axisLabel: { formatter: '{value}' }
    },
    yAxis: {
      type: 'value',
      min: 0,
      max: 100,
      axisLabel: { formatter: '{value}' }
    },
    grid: {
      left: '10%',
      right: '10%',
      bottom: '10%',
      top: '10%'
    },
    series: [
      {
        name: 'Interpolierte Kurve',
        type: 'line',
        data: dataLine,
        smooth: true,
        lineStyle: { color: '#000' },
        showSymbol: false,
        // Definiere farbige Bereiche (markArea) analog zu den axvspan-Bereichen
        markArea: {
          silent: true,
          data: [
            // [Start, Ende] jeweils als { xAxis, yAxis } – y von 0 bis 100
            [{ xAxis: 0.001, yAxis: 0, itemStyle: { color: 'rgba(128,128,128,0.2)' } }, { xAxis: 0.002, yAxis: 100 }],
            [{ xAxis: 0.002, yAxis: 0, itemStyle: { color: 'rgba(0,128,0,0.1)' } }, { xAxis: 0.0063, yAxis: 100 }],
            [{ xAxis: 0.0063, yAxis: 0, itemStyle: { color: 'rgba(0,128,0,0.2)' } }, { xAxis: 0.02, yAxis: 100 }],
            [{ xAxis: 0.02, yAxis: 0, itemStyle: { color: 'rgba(0,128,0,0.3)' } }, { xAxis: 0.063, yAxis: 100 }],
            [{ xAxis: 0.063, yAxis: 0, itemStyle: { color: 'rgba(255,165,0,0.1)' } }, { xAxis: 0.2, yAxis: 100 }],
            [{ xAxis: 0.2, yAxis: 0, itemStyle: { color: 'rgba(255,165,0,0.2)' } }, { xAxis: 0.63, yAxis: 100 }],
            [{ xAxis: 0.63, yAxis: 0, itemStyle: { color: 'rgba(255,165,0,0.3)' } }, { xAxis: 2, yAxis: 100 }],
            [{ xAxis: 2, yAxis: 0, itemStyle: { color: 'rgba(0,0,255,0.1)' } }, { xAxis: 6.3, yAxis: 100 }],
            [{ xAxis: 6.3, yAxis: 0, itemStyle: { color: 'rgba(0,0,255,0.2)' } }, { xAxis: 20, yAxis: 100 }],
            [{ xAxis: 20, yAxis: 0, itemStyle: { color: 'rgba(0,0,255,0.3)' } }, { xAxis: 63, yAxis: 100 }],
            [{ xAxis: 63, yAxis: 0, itemStyle: { color: 'rgba(128,128,128,0.3)' } }, { xAxis: 200, yAxis: 100 }]
          ]
        },
        // Zeichnet vertikale Hilfslinien an den angegebenen Siebdurchmessern
        markLine: {
          symbol: 'none',
          lineStyle: { type: 'dashed', width: 1 },
          data: [
            { xAxis: 0.002 },
            { xAxis: 0.006 },
            { xAxis: 0.02 },
            { xAxis: 0.063 },
            { xAxis: 0.2 },
            { xAxis: 0.63 },
            { xAxis: 2.0 },
            { xAxis: 6.3 },
            { xAxis: 20 },
            { xAxis: 63 }
          ]
        }
      },
      {
        name: 'Originaldaten',
        type: 'scatter',
        data: originalData,
        itemStyle: { color: '#000' }
      },
      {
        name: 'Wichtige Punkte',
        type: 'scatter',
        data: [
          [d10, 10],
          [d30, 30],
          [d60, 60]
        ],
        itemStyle: { color: 'red' },
        label: {
          show: true,
          fontSize: 18,
          color: 'red',
          formatter: function(params) {
            if (params.data[1] === 10) {
              return 'd10 = ' + d10.toFixed(3) + ' mm';
            } else if (params.data[1] === 30) {
              return 'd30 = ' + d30.toFixed(3) + ' mm';
            } else if (params.data[1] === 60) {
              return 'd60 = ' + d60.toFixed(3) + ' mm';
            }
            return '';
          }
        }
      },
      {
        // Zusätzliche Annotationen (Gradationscharakterisierung)
        name: 'Annotations',
        type: 'scatter',
        data: [],
        markPoint: {
          symbol: 'none',
          label: {
            fontSize: 18,
            color: '#000'
          },
          data: [
            {
              coord: [8, 12],
              label: { formatter: U_res + ':' }
            },
            {
              coord: [8, 5],
              label: { formatter: "C_U = " + U.toFixed(1) + ", C_C = " + Cc.toFixed(1) }
            }
          ]
        }
      }
    ]
  };

  return option;
}


const inputValues = [@input(`a`), @input(`b`), @input(`c`), @input(`d`), @input(`e`), @input(`f`), @input(`g`), @input(`h`), @input(`i`), @input(`j`), @input(`k`), @input(`l`)]
// Beispiel: 
// const inputValues = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120];
const siebdurchmesser = [63, 31.5, 16, 8, 4, 2, 1, 0.5, 0.25, 0.125, 0.063, 0.001];

// Erzeuge das ECharts‑Option-Objekt
"HTML: <lia-chart style='height: 500px;' option='" + JSON.stringify(plotKVKGlob(inputValues, siebdurchmesser)) + "'></lia-chart>"

// Anschließend kann das chartOption-Objekt an eine ECharts-Instanz übergeben werden, z.B.:
// const chart = echarts.init(document.getElementById('chart'));
// chart.setOption(chartOption);
</script>

## Lessons Learned



+ Die Interation von purem Python Code ist mit PyScript unglaublich einfach geworden.
+ Die in den Notebooks verwendenten Bibliotheken (`matplotlib`, `scipy`, `numpy`) sind in PyScript verfügbar, die Dauer des Ladens ist vertretbar.
+ Die Bibliotheken mussten in der angegebenen Reihung eingebunden werden, weil es sonst einen Fehler für Scipy gab.

  ``` 
     - matplotlib
     - scipy
     - numpy
  ```

+ Die Widgets es notwendig javascript Code für die Generierung des PyScript Blockes mit variablen Parametern zu verwenden. Darunter leidet die Les- und Testbarkeit des Codes. 
+ Die Berechnungsdauer für die Grafik beträgt etwa 2 Sekunden. 


