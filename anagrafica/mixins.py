from django.contrib.auth.mixins import UserPassesTestMixin

# Documentazione Mixins:
# https://docs.djangoproject.com/en/dev/topics/class-based-views/mixins/
# https://docs.djangoproject.com/en/dev/topics/auth/default/#django.contrib.auth.mixins.UserPassesTestMixin

class StaffMixin(UserPassesTestMixin):
    """
    Lo scopo di questo mixin è fare in modo che solo lo staff possa creare nuove sezioni
    Il test può considerarsi superato se la funzione test_func() restituisce valore booleano True
    """

    def test_func(self):
        return self.request.user.is_staff
