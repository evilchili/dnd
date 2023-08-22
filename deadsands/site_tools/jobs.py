import random
import collections

from npc.generator.base import generate_npc


Crime = collections.namedtuple('Crime', ['name', 'min_bounty', 'max_bounty'])


class BaseJob:
    """
    The base class for random odd jobs.
    """
    def __init__(
        self,
        name=None,
        details=None,
        reward=None,
        contact=None,
        location=None
    ):
        self._name = name
        self._details = details
        self._reward = reward
        self._contact = contact
        self._location = location

    @property
    def name(self):
        return self._name

    @property
    def details(self):
        if not self._details:
            self._details = (
                f"Speak to {self.contact} in {self.location}. "
            )
        return self._details

    @property
    def reward(self):
        return self._reward

    @property
    def contact(self):
        return self._contact

    @property
    def location(self):
        return self._location

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.name}\n{self.details}"


class Bounty(BaseJob):
    """
    A Bounty job.
    """

    crimes = [
        Crime(name='theft', min_bounty=50, max_bounty=500),
        Crime(name='overdue faction fees', min_bounty=50, max_bounty=500),
        Crime(name='unpaid bar tab', min_bounty=50, max_bounty=100),
        Crime(name="unpaid debt", min_bounty=50, max_bounty=200),
        Crime(name='cattle rustling', min_bounty=200, max_bounty=1000),
        Crime(name='murder', min_bounty=500, max_bounty=2000),
        Crime(name='kidnapping', min_bounty=500, max_bounty=2000)
    ]

    def __init__(self, target=None, crime=None, dead=None, alive=None, **kwargs):
        super().__init__(**kwargs)

        self._target = target

        self._crime = crime

        dead_or_alive = []
        if dead is None:
            dead = random.choice([True, False])
        if alive is None:
            alive = True
        if dead:
            dead_or_alive.append('Dead')
        if alive:
            dead_or_alive.append('Alive')
        self._dead_or_alive = ' or '.join(dead_or_alive)

        if not self._reward:
            # need to round to the nearest 10 < 100, nearest 100 otherwise
            reward = round(random.randint(self.crime.min_bounty, self.crime.max_bounty), 5)
            self._reward = f"{reward} Gold Pieces"

        if not self._name:
            self._name = (
                f"{self.reward} for the capture of {self.target.full_name.upper()}, "
                f"wanted for the crime of {self.crime.name.upper()}. "
                f"Wanted {self._dead_or_alive.upper()}"
            )

    @property
    def crime(self):
        if not self._crime:
            self._crime = random.choice(Bounty.crimes)
        return self._crime

    @property
    def details(self):
        if not self._details:
            self._details = f"{self.target.description}\nWhereabouts {self.target.whereabouts}."
        return self._details

    @property
    def target(self):
        if not self._target:
            self._target = generate_npc()
        return self._target


classes = BaseJob.__subclasses__()
job_types = [c.__name__ for c in classes]


def generate_job():
    return random.choice(classes)()


if __name__ == '__main__':
    print(Bounty())
