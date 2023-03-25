import click
if __name__ == '__main__':
    text = click.prompt(u"Give me input: ", prompt_suffix='')
    click.echo(u"Do you mean '{0}'?".format(text))