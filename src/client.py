import click
from src.service import *


@click.group()
@click.pass_context
def googlecal(ctx):
    ctx.obj = {'Done by Ernar Kusdavletov on Sep 2018'}


@click.command(help='Sign in to Google Calendar')
@click.pass_context
def login(ctx):
    sign_in()


@click.command(help='Get a schedule')
@click.option('--date', type=str, default='', help='Specific date to print')
@click.option('--number', type=int, default=7, help='Number of days to print')
@click.pass_context
def schedule(ctx, date, number):
    get_schedule(date, number)


@click.command(help='Add new event')
@click.pass_context
def add(ctx):
    add_event_quick()


@click.command(help='Add new event (detailed)')
@click.pass_context
def add_advanced(ctx):
    add_event_advanced()


@click.command(help='Get an id from event name')
@click.argument('name', type=str)
@click.pass_context
def get_id(ctx, name):
    get_id_from_name(name)


@click.command(help='Edit event with id')
@click.argument('id', type=str)
@click.pass_context
def edit(ctx, id):
    edit_event(id)


@click.command(help='Delete event with id')
@click.argument('id', type=str)
@click.pass_context
def delete(ctx, id):
    delete_event(id)


googlecal.add_command(login)
googlecal.add_command(schedule)
googlecal.add_command(add)
googlecal.add_command(add_advanced)
googlecal.add_command(get_id)
googlecal.add_command(edit)
googlecal.add_command(delete)
