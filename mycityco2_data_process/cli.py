import typer

cli = typer.Typer(no_args_is_help=True)


@cli.callback()
def callback():
    """
    MyCityCo2 data processing script
    """
