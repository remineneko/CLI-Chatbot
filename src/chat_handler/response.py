class ChatResponse:
    """ An object to simplify response JSON/object from the given completion.
    """

    __slots__ = (
        'id',
        'object',
        'created',
        'choices',
        'usage'
    )

    def __init__(self, response):
        self._full_info = response
        for key in self.__slots__:
            self.__setattr__(key, response.key if key in response else None)

    @property
    def raw_response(self):
        return self._full_info
    
    @property
    def answer(self):
        try:
            return self.choices[0].message.content
        except AttributeError:
            return self.choices[0].text
        
    @property
    def role(self):
        try:
            return self.choices[0].message.role
        except AttributeError:
            return None

    def __eq__(self, o):
        if isinstance(o, ChatResponse):
            if self.id == o.id:
                return True
            else:
                return False
        else:
            return False