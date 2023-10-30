from src.abstractions.db_creator import DBCreator, ConfirmationException
from src.data_managers.db_creator_pg import DBCreatorPG
from src.utils.console_color import FG_YELLOW, FG_RESET, FG_RED, FG_GREEN


def user_interaction(db_creator: DBCreator):

    for prop in db_creator:
        while True:
            try:
                prompt = f'{prop.description}{(f" [{FG_GREEN}{prop}{FG_RESET}]" if prop.value else "")}: '

                new_value = input(prompt)

                if new_value:
                    prop.value = new_value
                else:
                    prop.value = prop.value  # for validation
                break

            except TypeError as te:
                print(f'{FG_RED}{te}{FG_RESET}')

            except ConfirmationException as ce:
                print(f'{FG_YELLOW}{ce}{FG_RESET}')
                if input(f'Continue? (y/n): ').lower() == 'y':
                    break

    try:
        db_creator.init_database()
        print(f'{FG_GREEN}Database init success!{FG_RESET}')
        return False

    except Exception as ex:
        print(f'{FG_YELLOW}Database init failed!{FG_RESET}\n')
        print(f'{FG_RED}{ex}{FG_RESET}')
        return True


if __name__ == '__main__':

    try:
        db_creator: DBCreator = DBCreatorPG()
        while user_interaction(db_creator):
            pass
    except KeyboardInterrupt:
        print(f'\n\n{FG_YELLOW}Database init aborted{FG_RESET}')
