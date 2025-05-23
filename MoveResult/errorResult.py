from MoveResult.baseResult import BaseResult

class ErrorResult(BaseResult):
    pass

# class InvalidCardOwner(ErrorResult):
#     def __str__(self):
#         return "This card does not belong to you"

class SuitDuplicated(ErrorResult):
    def __str__(self):
        return "This card suit is already in trick"