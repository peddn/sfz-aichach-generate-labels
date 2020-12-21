import os
import click
from pathlib import Path
import csv

from bs4 import BeautifulSoup

os.chdir('data')

def validate_input(ctx, param, value):
    try:
        with open(value, 'r') as file:
            file.close()
            return(value)
        
    except EnvironmentError as err: # parent of IOError, OSError *and* WindowsError where available
        raise click.BadParameter(str(err))

def validate_output(ctx, param, value):
    try:
        with open(value, 'w') as file:
            file.close()
            return(value)
    except EnvironmentError as err: # parent of IOError, OSError *and* WindowsError where available
        raise click.BadParameter(str(err))     


@click.command()
@click.option('--html_file', callback=validate_input, default='labels.html', help='The input HTML file.')
@click.option('--csv_file', callback=validate_output, default='labels.csv', help='The output CSV file.')
def gen_labels(html_file, csv_file):
    """A python script to generate csv out of a saved snipe-it labels web page.

    \b
    The default html input file is './data/lables.html'
    The default csv output file is './data/labels.csv'
    """

    click.echo('data directory: ' + os.getcwd())

    html_path = Path(html_file)
    csv_path  = Path(csv_file)

    click.echo('input html file: %s' % str(html_path))
    click.echo('output csv file: %s' % str(csv_path))

    html_str = None

    try:
        with open(html_path, 'r') as file:
            html_str = file.read()
    except EnvironmentError as err: # parent of IOError, OSError *and* WindowsError where available
        raise click.ClickException(str(err))

    soup = BeautifulSoup(html_str, 'html.parser')

    # print(soup.prettify())

    click.echo('Writing ' + str(csv_path) + ' ...')
    try:
        with open(csv_path, 'w', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(['qr_code_image_path', 'asset_id', 'serial_nr', 'model_nr'])
            for div in soup.find_all('div', class_='label'):

                qr_code_path = str(Path(div.div.img['src']).resolve()).strip()
                asset_id = div.div.next_sibling.next_sibling.div.get_text().strip()[3:]
                serial_nr = div.div.next_sibling.next_sibling.div.next_sibling.next_sibling.get_text().strip()[3:]
                model_nr = div.div.next_sibling.next_sibling.div.next_sibling.next_sibling.next_sibling.next_sibling.get_text().strip()[3:]

                csv_writer.writerow([qr_code_path, asset_id, serial_nr, model_nr])

    except EnvironmentError as err: # parent of IOError, OSError *and* WindowsError where available
        raise click.ClickException(str(err))

    click.echo('Success.')

if __name__ == '__main__':
    gen_labels()
