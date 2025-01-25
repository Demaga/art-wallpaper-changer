from dataclasses import dataclass


@dataclass(repr=False)
class Artwork:
    url: str
    title: str | None = None
    culture: str | None = None
    period: str | None = None
    artist: str | None = None
    date: str | None = None

    def __repr__(self):
        text = ""
        if self.title:
            text += f"Title: {self.title}\n"
        if self.culture:
            text += f"Culture: {self.culture}\n"
        if self.period:
            text += f"Period: {self.period}\n"
        if self.artist:
            text += f"Artist: {self.artist}\n"
        if self.date:
            text += f"Date: {self.date}"
        return text
