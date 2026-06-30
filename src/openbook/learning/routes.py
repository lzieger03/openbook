from .viewsets.state       import LearningStateViewSet
from .viewsets.quiz_result import QuizResultViewSet

def register_api_routes(router, prefix):
    router.register(f"{prefix}/states",       LearningStateViewSet, basename="learning-state")
    router.register(f"{prefix}/quiz-results", QuizResultViewSet,    basename="quiz-result")
