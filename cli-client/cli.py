#!/usr/bin/python3

import click
import requests
import json, os


@click.group(invoke_without_command=True)
def cli():
    """
    Welcome to CLI client for charge EVolution app. See the options below.

    """


@cli.command()
def greeting():
    """Greeting the user"""
    click.secho("""Welcome to,
    
      _                            ________      __   _       _   _             
     | |                          |  ____\ \    / /  | |     | | (_)            
  ___| |__   __ _ _ __ __ _  ___  | |__   \ \  / /__ | |_   _| |_ _  ___  _ __  
 / __| '_ \ / _` | '__/ _` |/ _ \ |  __|   \ \/ / _ \| | | | | __| |/ _ \| '_ \ 
| (__| | | | (_| | | | (_| |  __/ | |____   \  / (_) | | |_| | |_| | (_) | | | |
 \___|_| |_|\__,_|_|  \__, |\___| |______|   \/ \___/|_|\__,_|\__|_|\___/|_| |_|
                       __/ |                                                    
                      |___/                                                     
""", fg="blue", bold=True) #\U0001F699


baseURL = "http://localhost:5000/api"

@cli.command()
@click.option('--format', type = click.Choice(['json', 'csv']), default = 'json', 
              help = 'Choose the format between json and csv.', required = True)
def healthcheck(format):
    """Check the end-to-end connectivity with the DBMS."""
    data = requests.get(f'{baseURL}/admin/healthcheck?format={format}')
    print(data.text)

@cli.command()
@click.confirmation_option(prompt = 'Are you sure you want to drop the sessions table?')
def resetsessions(format):
    """Initialize sessions table and the default moderator's account"""
    data = requests.post(f'{baseURL}/admin/resetsessions')
    print(data.text)

@cli.command()
@click.option('--username', '-U', type = click.STRING, required = True,
             help = 'Give your username')
@click.option('--passw', '-P', type = click.STRING, required = True,
             help='Give your password')
def login(username, passw):
    """"Login to the app, username and password are required. Use the returned token in the apikey parameter for the rest commands"""
    credentials = json.dumps({
                    'username': username,
                    'password': passw
                  })

    headers = {
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", f'{baseURL}/users/login', headers=headers, data=credentials)
    data = response.json()
    print(data)
    if data['status'] == 200:
        click.echo("You have successfully logged in, copy your token for next use")
        hdir = os.path.expanduser('~')
        charge_ev_token = data['token']
        with open(f'{hdir}/.softeng20bAPI.token', "w") as t:
            t.write(f'[Verified User]\n\tusername={username}\n\tcharge_evolution_token={charge_ev_token}')
    else:
        click.echo("Please, try again.")


@cli.command()
@click.option('--apikey', type = click.STRING, required = True,
              help = 'Give your log-in token')
def logout(apikey):
    """Log out from the app. A valid token is required."""
    headers = {
                'charge_evolution_token': apikey
            }
    response = requests.request("POST", f'{baseURL}/users/logout', headers=headers)
    data = response.json()
    print(data)
    if data['status'] == 200:
        click.echo("Logged out successfully. Have a great day!")
        hdir = os.path.expanduser('~')
        os.remove(f'{hdir}/.softeng20bAPI.token') 
    else:
        click.echo("Please, try again.")  


@cli.command()
@click.option('--point', type = click.STRING, required = True,
              help = 'Give the ID of the point')
@click.option('--datefrom', '-F', type = click.DateTime(), default = '2010-01-01',
              help = 'Give the required date (from)')
@click.option('--dateto', '-T', type = click.DateTime(), default = '2025-01-01',
              help = 'Give the required daet(to)')
@click.option('--format', type = click.Choice(['json', 'csv']), default = 'json', 
              help = 'Choose between json and csv format', required = True)
@click.option('--apikey', type = click.STRING, required = True,
              help = 'Give your log-in token')
def sessionsPerPoint(point,datefrom,dateto,format,apikey):
    """Show sessions for a specific vehicle and period of time"""
    headers = {'charge_evolution_token': apikey}
    response = requests.request("GET", f'{baseURL}/sessions/point/{point}/{datefrom}/{dateto}?format={format}', headers=headers)
    print(response.text)


@cli.command()
@click.option('--station','-S', type = click.STRING, required = True,
              help = 'Give the ID of the station')
@click.option('--datefrom', '-F', type = click.DateTime(), default = '2010-01-01',
              help = 'Give the required date (from)')
@click.option('--dateto', '-T', type = click.DateTime(), default = '2025-01-01',
              help = 'Give the required daet(to)')
@click.option('--format', type = click.Choice(['json', 'csv']), default = 'json', 
              help = 'Choose between json and csv format', required = True)
@click.option('--apikey', type = click.STRING, required = True,
              help = 'Give your log-in token')
def sessionsPerStation(station,datefrom,dateto,format,apikey):
    """Show sessions for a specific vehicle and period of time"""
    headers = {'charge_evolution_token': apikey}
    response = requests.request("GET", f'{baseURL}/sessions/station/{station}/{datefrom}/{dateto}?format={format}', headers=headers)
    print(response.text)


@cli.command()
@click.option('--vehicle','-EV', type = click.STRING, required = True,
              help = 'Give the ID of the vehicle')
@click.option('--datefrom', '-F', type = click.DateTime(), default = '2010-01-01',
              help = 'Give the required date (from)')
@click.option('--dateto', '-T', type = click.DateTime(), default = '2025-01-01',
              help = 'Give the required daet(to)')
@click.option('--format', type = click.Choice(['json', 'csv']), default = 'json', 
              help = 'Choose between json and csv format')
@click.option('--apikey', type = click.STRING, required = True,
              help = 'Give your log-in token')
def sessionsPerEV(vehicle,datefrom,dateto,format,apikey):
    """Show sessions for a specific vehicle and period of time"""
    headers = {'charge_evolution_token': apikey}
    response = requests.request("GET", f'{baseURL}/sessions/ev/{vehicle}/{datefrom}/{dateto}?format={format}', headers=headers)
    print(response.text)


@cli.command()
@click.option('--provider', type = click.STRING, required = True,
              help = 'Give the providers ID')
@click.option('--datefrom', '-F', type = click.DateTime(), default = '2010-01-01',
              help = 'Give the required date (from)')
@click.option('--dateto', '-T', type = click.DateTime(), default = '2025-01-01',
              help = 'Give the required daet(to)')
@click.option('--format', type = click.Choice(['json', 'csv']), default = 'json', 
              help = 'Choose between json and csv format', required = True)
@click.option('--apikey', type = click.STRING, required = True,
              help = 'Give your log-in token')
def sessionsPerProvider(provider,datefrom,dateto,format,apikey):
    """Show sessions for a specific vehicle and period of time"""
    headers = {'charge_evolution_token': apikey}
    response = requests.request("GET", f'{baseURL}/sessions/provider/{provider}/{datefrom}/{dateto}?format={format}', headers=headers)
    print(response.text)


@cli.command()
@click.option('--usermod', is_flag = True, help = 'Use this flag parameter to create new user or change password.')
@click.option('--users', is_flag = True, help = 'Use this flag parameter to view users state.')
@click.option('--sessionsupd','-S', is_flag = True, help = 'Use this flag parameter to add sessions data from CSV file.')
@click.option('--source', type=click.Path(exists = True), help='Give the input file with sessions data.')
@click.option('--healthcheck', '-H', is_flag=True, help='Use this flag parameter to check the end-to-end connectivity with the DBMS.')
@click.option('--resetsessions','-r', is_flag = True, help = 'Use this flag parameter to initialize sessions table and the default moderators account')
@click.option('--format', type = click.Choice(['json', 'csv']), default = 'json', 
              help = 'Choose between json and csv format')
@click.option('--apikey', type = click.STRING, required = True,
              help = 'Give your log-in token')
@click.option('--username', '-U', type=click.STRING, 
              help = 'Give your new/existing username', required = False) #prompt = 'Your username is required, please',
@click.option('--passw', '-P', type=click.STRING, help = 'Give your new/existing password')#, prompt = 'Your password is required, please',
              
def Admin(usermod,username,passw,users,sessionsupd,source,healthcheck,resetsessions,format,apikey):
    """Command for administrator. Functionality depends on the chosen flag. See more info below."""
    flag = False
    for x in [usermod,users,sessionsupd,healthcheck,resetsessions]:
        if x is not None:
            if flag == True and x == True: 
                raise click.ClickException('Please use only one flag.')
            elif x == True or type(x) == str: 
                flag = True 
    if flag == False: raise click.UsageError('Please choose one flag.')
    else:
        headers = {'charge_evolution_token': apikey}
        if usermod:
            if username is not None and passw is not None:
                first_name = click.prompt('Please enter your first name')
                last_name = click.prompt('Please enter your last name')
                tel = click.prompt('Please enter your telephone number')
                email = click.prompt('Please enter your email')
                payload = json.dumps({
                    'first_name': first_name,
                    'last_name': last_name, 
                    'telephone_number': tel,
                    'email': email
                })
                headerss = {
                            'charge_evolution_token': apikey,
                            'Content-Type': 'application/json'
                }
                response = requests.request("POST", f'{baseURL}/admin/usermod/{username}/{passw}', headers=headerss, data = payload)
                print(response.text)
                if format != 'csv' :
                    data = response.json()
                    if data['status'] == 200:
                        print('You have successfully registered as admin!')
                    else:
                        print('Please check the information you have given and try again.')
            else: raise click.BadParameter('You have to provide both the username and the password.',param_hint='username, passw')
        elif users:
            if username is None:
                raise click.BadParameter('You have to provide the username.', username)
            else:
                response = requests.request("GET", f'{baseURL}/admin/users/{username}', headers=headers)
                click.echo(response.text)               
        elif sessionsupd:
            if source is not None:
                payload={}
                files = [('file',('sessions.csv',open('{source}','rb'),'text/csv'))]
                response = requests.request("GET", f'{baseURL}/admin/system/sessionsupd', headers=headers, data=payload, files=files)
                print(response.text)
            else: raise click.BadParameter('You have to provide the source file. See --source parameter below', source)
        elif healthcheck:
            data = requests.get(f'{baseURL}/admin/healthcheck?format={format}')
            print(data.text)
        elif resetsessions:
            data = requests.post(f'{baseURL}/admin/system/resetsessions')
            print(data.text)


@cli.command()
@click.option('--upload', is_flag = True, help = "Use this flag parameter to upload a csv file with new station's data.")
@click.option('--delete', is_flag = True, help = "Use this flag parameter to delete a station from DBMS.")
@click.option('--source', type=click.Path(exists = True), help="Give the input file with station's data.")
@click.option('--station','-S', type = click.STRING, help = 'Give the ID of the station')
@click.option('--apikey', type = click.STRING, required = True,
              help = 'Give your log-in token')
def modstation(upload,delete,source,station, apikey):
    """Command for administrator to manage stations. Upload a csv file to add a new station or give station_id to delete an existing station. See more info below"""
    if upload and delete: raise click.UsageError('Please choose only one flag.')
    elif not upload and not delete: raise click.UsageError('Please choose one flag.')
    else:
        headers = {'charge_evolution_token': apikey}
        if upload:
            if source is not None:
                payload={}
                files = [('file',('station.csv',open('{source}','rb'),'text/csv'))]
                response = requests.request("GET", f'{baseURL}/admin/system/newstation', headers=headers, data=payload, files=files)
                print(response.text)
            else: raise click.BadParameter('You have to provide the source file. See --source parameter below', source)
        else:
            if station is not None:
                response = requests.request("POST",  f'{baseURL}/admin/system/deletestation/{station}', headers=headers)
                print(response.text)
            else: raise click.BadParameter('You have to provide the station id.', station)


if __name__ == "__main__":
    cli()
