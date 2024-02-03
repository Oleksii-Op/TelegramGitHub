from plotly.graph_objs import Bar, Layout
from plotly import offline
import plotly.io as pio
from io import BytesIO
from PIL import Image
from die import Die
from typing import Optional


def main(number_of_rolls: Optional[int] = 5000) -> None:
    """Main function. Creating 2 dies and rolling them."""
    die_1 = Die()
    die_2 = Die()

    # Modeling a series of rolls and saving the results in a list.
    results = [die_1.roll() + die_2.roll() for _ in range(number_of_rolls)]

    # Results analysis
    max_result = die_1.num_sides + die_2.num_sides
    frequencies = [results.count(value) for value in range(2, max_result + 1)]


    # Visualization of results.
    x_values = list(range(2, max_result + 1))
    data = [Bar(x=x_values, y=frequencies)]

    x_axis_config = {'title': 'Результат суммы 2х 6ти гранных'
                              ' кубиков', 'dtick': 1}

    y_axis_config = {'title': 'Частота'}

    my_layout = Layout(title=f'Результаты броска 2х 6ти гранных'
                             f' кубиков {number_of_rolls} раз',
                             xaxis=x_axis_config, yaxis=y_axis_config)

    offline.plot({'data': data, 'layout': my_layout}, filename='d6_1.html', auto_open=False)

    # Converting plotly image to PIL image and saving it.
    image_bytes = pio.to_image({'data': data, 'layout': my_layout},
                               format='png', engine='kaleido', width=1000, height=800)

    image = Image.open(BytesIO(image_bytes))
    image.save('d6_1.png', format='PNG')


if __name__ == '__main__':
    main()
