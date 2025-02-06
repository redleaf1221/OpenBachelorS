import traceback

import click
from prompt_toolkit import PromptSession

from ..util.player_data import PlayerData, player_data_template
from ..util.helper import get_char_num_id


@click.group(invoke_without_command=True)
@click.option("--interactive", "-i", is_flag=True)
@click.pass_context
def cli(ctx, interactive):
    ctx.ensure_object(dict)

    if interactive:
        session = PromptSession()

        while True:
            try:
                text = session.prompt("> ")
            except KeyboardInterrupt:
                continue
            except EOFError:
                break

            try:
                argv = text.split()
                cli(argv, standalone_mode=False)
            except Exception:
                traceback.print_exc()

        exit()


def configure_current_equip(player_data, char_num_id, evolve_phase):
    char_obj = player_data["troop"]["chars"][str(char_num_id)]
    if "tmpl" in char_obj:
        for tmpl_id, tmpl_obj in char_obj["tmpl"]:
            if evolve_phase < 2:
                current_equip = None
            else:
                current_equip = player_data_template["troop"]["chars"][
                    str(char_num_id)
                ]["tmpl"][tmpl_id]["currentEquip"]

            tmpl_obj["currentEquip"] = current_equip
    else:
        if evolve_phase < 2:
            current_equip = None
        else:
            current_equip = player_data_template["troop"]["chars"][str(char_num_id)][
                "currentEquip"
            ]
        char_obj["currentEquip"] = current_equip


@cli.command()
@click.option("-p", "--player-id", required=True)
@click.option("-c", "--char-id", required=True)
@click.option("--potential-rank", type=int)
@click.option("--favor-point", type=int)
@click.option("--evolve-phase", type=int)
@click.option("--level", type=int)
@click.option("--main-skill-lvl", type=int)
@click.option("--skill-idx", "skill_idx_lst", multiple=True, type=int)
@click.option("--specialize-level", type=int)
@click.option("--equip-id", "equip_id_lst", multiple=True)
@click.option("--equip-level", type=int)
@click.option("--tmpl-id")
@click.pass_context
def char(
    ctx,
    player_id,
    char_id,
    potential_rank,
    favor_point,
    evolve_phase,
    level,
    main_skill_lvl,
    skill_idx_lst,
    specialize_level,
    equip_id_lst,
    equip_level,
    tmpl_id,
):
    player_data = PlayerData(player_id)

    char_num_id = get_char_num_id(char_id)

    if potential_rank is not None:
        player_data["troop"]["chars"][str(char_num_id)]["potentialRank"] = (
            potential_rank
        )

    if favor_point is not None:
        player_data["troop"]["chars"][str(char_num_id)]["favorPoint"] = favor_point

    if evolve_phase is not None:
        player_data["troop"]["chars"][str(char_num_id)]["evolvePhase"] = evolve_phase
        configure_current_equip(player_data, char_num_id, evolve_phase)

    if level is not None:
        player_data["troop"]["chars"][str(char_num_id)]["level"] = level

    if main_skill_lvl is not None:
        player_data["troop"]["chars"][str(char_num_id)]["mainSkillLvl"] = main_skill_lvl

    if skill_idx_lst:
        if specialize_level is not None:
            if tmpl_id is None:
                for skill_idx in skill_idx_lst:
                    skill_lst = player_data["troop"]["chars"][str(char_num_id)][
                        "skills"
                    ].copy()
                    skill_lst[skill_idx]["specializeLevel"] = specialize_level
                    player_data["troop"]["chars"][str(char_num_id)]["skills"] = (
                        skill_lst
                    )
            else:
                for skill_idx in skill_idx_lst:
                    skill_lst = player_data["troop"]["chars"][str(char_num_id)]["tmpl"][
                        tmpl_id
                    ]["skills"].copy()
                    skill_lst[skill_idx]["specializeLevel"] = specialize_level
                    player_data["troop"]["chars"][str(char_num_id)]["tmpl"][tmpl_id][
                        "skills"
                    ] = skill_lst

    if equip_id_lst:
        if equip_level is not None:
            if tmpl_id is None:
                for equip_id in equip_id_lst:
                    player_data["troop"]["chars"][str(char_num_id)]["equip"][equip_id][
                        "level"
                    ] = equip_level
            else:
                for equip_id in equip_id_lst:
                    player_data["troop"]["chars"][str(char_num_id)]["tmpl"][tmpl_id][
                        "equip"
                    ][equip_id]["level"] = equip_level

    player_data.save()


@cli.group()
@click.pass_context
def sandbox(
    ctx,
):
    pass


@sandbox.command()
@click.pass_context
def enemy_rush(
    ctx,
):
    pass


if __name__ == "__main__":
    cli()
