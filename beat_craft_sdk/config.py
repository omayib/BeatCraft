class Config:
    def __init__(self, tempo="medium",vibe="neutral"):
        self.tempo = tempo
        self.vibe = vibe
        self.validate_config()
        print(f"init config tempo {self.tempo}")

    def validate_config(self):
        valid_tempos = ["slow","medium","fast"]
        valid_vibes = ["calm","neutral","stress"]

        if self.tempo not in valid_tempos:
            raise ValueError(f"Invalid tempo : {self.tempo}. Must be one of {valid_tempos}")
        if self.vibe not in valid_vibes:
            raise ValueError(f"Invalid vibe : {self.vibe}. Must be on if {valid_vibes}")

    def __repr__(self):
        return f"Config(tempot='{self.tempo}', vibe='{self.vibe}')"

    def to_dict(self):
        return {"tempo":self.tempo, "vibe":self.vibe}