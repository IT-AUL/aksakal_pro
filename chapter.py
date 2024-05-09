class Chapter:
    def __init__(self, chapter_id, title, quest):
        self.chapter_id = chapter_id
        self.title = title
        self.quest = quest
        self.current_quest_id = quest[0].id
