from django import forms
from utils.query import *

PILIHAN_ROLE = [('Podcaster', 'Podcaster'), ('Artist', 'Artist'), ('Songwriter', 'Songwriter')]

class RegisterFormPengguna(forms.Form):
    email = forms.EmailField(label='Email', max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Email', 'oninvalid': "this.setCustomValidity('Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu')", 'oninput': "setCustomValidity('')"}))
    password = forms.CharField(label='Password', max_length=50, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': '***********', 'oninvalid': "this.setCustomValidity('Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu')", 'oninput': "setCustomValidity('')"}))
    nama = forms.CharField(label='Nama', max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Nama', 'oninvalid': "this.setCustomValidity('Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu')", 'oninput': "setCustomValidity('')"}))
    gender = forms.ChoiceField(label='Gender', choices=[(1, 'Laki-laki'), (0, 'Perempuan')], widget=forms.Select(
        attrs={'class': 'border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 mt-2', 'placeholder': 'Jenis Kelamin', 'oninvalid': "this.setCustomValidity('Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu')", 'oninput': "setCustomValidity('')"}))
    tempat_lahir = forms.CharField(label='Tempat Lahir', max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Tempat Lahir', 'oninvalid': "this.setCustomValidity('Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu')", 'oninput': "setCustomValidity('')"}))
    tanggal_lahir = forms.DateField(label='Tanggal Lahir', widget=forms.DateInput({
                                    'class': 'form-control', 'type': 'date'}))
    kota_asal = forms.CharField(label='Kota Asal', max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Kota Asal', 'oninvalid': "this.setCustomValidity('Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu')", 'oninput': "setCustomValidity('')"}))
    role = forms.MultipleChoiceField(label='Role', choices=PILIHAN_ROLE, required=False, widget=forms.CheckboxSelectMultiple(
        attrs={'class': 'form-check-input', 'oninput': "setCustomValidity('')"}))
    
class RegisterFormLabel(forms.Form):
    email = forms.EmailField(label='Email', max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Email', 'oninvalid': "this.setCustomValidity('Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu')", 'oninput': "setCustomValidity('')"}))
    password = forms.CharField(label='Password', max_length=50, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': '***********', 'oninvalid': "this.setCustomValidity('Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu')", 'oninput': "setCustomValidity('')"}))
    nama = forms.CharField(label='Nama', max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Nama', 'oninvalid': "this.setCustomValidity('Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu')", 'oninput': "setCustomValidity('')"}))
    kontak = forms.CharField(label='Kontak', max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Kontak', 'oninvalid': "this.setCustomValidity('Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu')", 'oninput': "setCustomValidity('')"}))