from fastapi import HTTPException, status

class MainException(HTTPException): 
    status_code = 500  
    detail = "Неизвестная ошибка"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(MainException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"

class ObjectIsNotExists(MainException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Обьект не найден"

class RoomsIsNotExists(MainException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Комната не найдена"

class HotelsIsNotExists(MainException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Отель не найден"


class AllRoomsAreBooked(MainException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Все комнаты заняты"

class IncorrectDate(MainException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Дата заезда позже даты выезда"