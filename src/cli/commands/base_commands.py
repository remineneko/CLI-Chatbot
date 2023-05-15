from abc import abstractmethod, ABC
from typing import List


class Command(ABC):
    PREFIX = ">>"
    @abstractmethod
    def _get_commands(self) -> List[str]:
        """
        Gets the commands that will be used from the class.

        This is rather scuffed - I would prefer to learn a way that I could do this internally without having to
            explicitly declare this every time
        
        Returns a list of commands, preferably as string names.
        """
        pass

    def setup(self, cli):
        for command in self._get_commands():

            cli.add_command(getattr(self, command), name=self.PREFIX + command)
