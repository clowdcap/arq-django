from django.contrib.contenttypes import fields
from django.views.generic.list import ListView
from .models import Curso
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required

# Create your views here.

class DonoMixin(object):
    def get_queryset(self):
        q = super().get_queryset()
        return q.filter(dono=self.request.user)


class DonoEditarMixin(object):
    def form_valid(self, form):
        form.instance.dono = self.request.user
        return super().form_valid(form)


class DonoCursoMixin(DonoMixin, 
                     LoginRequiredMixin, 
                     PermissionRequiredMixin):
    model = Curso
    fields = ['assunto', 'titulo', 'slug', 'desc_geral']
    sucess_url = reverse_lazy('gerenciar_cursos_list')
    

class DonoCursoEditMixin(DonoCursoMixin, 
                         DonoEditarMixin):
    template_name = 'gerenciar/curso/form.html'



class ListarCursosListView(DonoCursoMixin, 
                           ListView):
    template_name = 'gerenciar/curso/listar.html'
    permission_required = 'protocolo.view_curso'



class CriarCursoCreateView(DonoCursoEditMixin, 
                           CreateView):
    permission_required = 'protocolo.add_curso'



class AtualizarCursoUpdateView(DonoCursoEditMixin, 
                               UpdateView):
    permission_required = 'protocolo.change_curso'


class ExcluirCursoDeleteView(DonoCursoMixin, 
                             DeleteView):
    template_name = 'gerenciar/curso/excluir.html'
    permission_required = 'protocolo.excluir_curso'


