import experiment1 as e1
import experiment2 as e2
import ManualStrategy as ms

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
if __name__ == "__main__":
    ms.msrun()
    e1.exp1run()
    e2.experiment2()

def author():
    return 'ydeng335'