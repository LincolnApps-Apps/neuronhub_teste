from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

class Endereco(models.Model):
    nome = models.CharField(max_length=100, null=True, blank=True)
    cep = models.CharField(max_length=8, validators=[RegexValidator(regex='^\d{8}$', message='CEP deve conter 8 dígitos.')])
    logradouro = models.CharField(max_length=100)
    complemento = models.CharField(max_length=100, null=True, blank=True)
    bairro = models.CharField(max_length=50)
    cidade = models.CharField(max_length=50)
    estado = models.CharField(max_length=2, validators=[RegexValidator(regex='^[A-Z]{2}$', message='Estado deve conter 2 letras maiúsculas.')])
    pais = models.CharField(max_length=50, default='Brasil')
    matriz = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.logradouro}, {self.cidade} - {self.estado}, {self.cep}"

class Cargo(models.Model):
    nome = models.CharField(max_length=50)
    descricao = models.TextField(null=True, blank=True)
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    beneficios = models.TextField(null=True, blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome

class Permissao(models.Model):
    nome = models.CharField(max_length=50)
    descricao = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nome

class CargoPermissao(models.Model):
    cargo = models.ForeignKey(Cargo, related_name='permissoes', on_delete=models.CASCADE)
    permissao = models.ForeignKey(Permissao, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.cargo.nome} - {self.permissao.nome}"

class Contato(models.Model):
    telefone = models.CharField(max_length=15, null=True, blank=True, validators=[RegexValidator(regex='^\+?1?\d{9,15}$', message='Telefone deve conter entre 9 e 15 dígitos.')])
    email = models.EmailField(null=True, blank=True)
    site = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.telefone if self.telefone else self.email

class Documento(models.Model):
    id_nacional = models.CharField(max_length=20, unique=True)
    rg = models.CharField(max_length=10, unique=True)
    certidao_nascimento = models.CharField(max_length=20, unique=True, null=True, blank=True)
    inscricao_estadual = models.CharField(max_length=20, unique=True, null=True, blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id_nacional

class DocumentoFile(models.Model):
    rg = models.FileField(upload_to='documentos/')
    certidao_nascimento = models.FileField(upload_to='documentos/', null=True, blank=True)
    inscricao_estadual = models.FileField(upload_to='documentos/', null=True, blank=True)
    cartao_cnpj = models.FileField(upload_to='documentos/', null=True, blank=True)
    contrato_social = models.FileField(upload_to='documentos/', null=True, blank=True)
    procuracao = models.FileField(upload_to='documentos/', null=True, blank=True)
    comprovante_endereco = models.FileField(upload_to='documentos/', null=True, blank=True)

    def __str__(self):
        return f"Documento {self.id}"

class InfoPessoal(models.Model):
    GENERO_CHOICES = [('M', 'Masculino'), ('F', 'Feminino'), ('O', 'Outro')]
    
    apelido = models.CharField(max_length=50)
    nascimento = models.DateField(null=True, blank=True)
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES)
    estado_civil = models.CharField(max_length=20)

    def __str__(self):
        return self.apelido

class InfoBancaria(models.Model):
    TIPO_CHOICES = [('P', 'Poupança'), ('C', 'Corrente')]
    
    banco = models.CharField(max_length=100)
    agencia = models.CharField(max_length=10)
    conta = models.CharField(max_length=20)
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)

    def __str__(self):
        return self.banco

class Veiculo(models.Model):
    placa = models.CharField(max_length=8, unique=True)
    marca = models.CharField(max_length=20)
    modelo = models.CharField(max_length=20)
    cor = models.CharField(max_length=20)
    ano = models.IntegerField(validators=[MinValueValidator(1886), MaxValueValidator(9999)])  # Carro mais antigo é de 1886

    def __str__(self):
        return self.placa

class Empresa(models.Model):
    razao_social = models.CharField(max_length=100)
    nome_fantasia = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=20, unique=True)
    inscricao_estadual = models.CharField(max_length=20, unique=True)
    inscricao_municipal = models.CharField(maxlength=20, unique=True, null=True, blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.razao_social

class EnderecoEmpresa(models.Model):
    empresa = models.ForeignKey(Empresa, related_name='enderecos', on_delete=models.CASCADE)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.empresa.razao_social} - {self.endereco}"

class ContatoEmpresa(models.Model):
    empresa = models.ForeignKey(Empresa, related_name='contatos', on_delete=models.CASCADE)
    contato = models.ForeignKey(Contato, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.empresa.razao_social} - {self.contato}"

class CargoEmpresa(models.Model):
    empresa = models.ForeignKey(Empresa, related_name='cargos', on_delete=models.CASCADE)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.empresa.razao_social} - {self.cargo}"

class DocumentoEmpresa(models.Model):
    empresa = models.ForeignKey(Empresa, related_name='documentos_files', on_delete=models.CASCADE)
    documentos = models.ForeignKey(DocumentoFile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.empresa.razao_social} - {self.documentos}"

class Departamento(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(null=True, blank=True)
    empresa = models.ForeignKey(Empresa, related_name='departamentos', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nome} - {self.empresa.razao_social}"

class Fornecedor(models.Model):
    nome = models.CharField(max_length=100)
    documentos = models.ForeignKey(Documento, on_delete=models.CASCADE, null=True, blank=True)
    info_pessoal = models.ForeignKey(InfoPessoal, on_delete=models.CASCADE, null=True, blank=True)
    preferencias = models.TextField(null=True, blank=True)
    observacoes = models.TextField(null=True, blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True)  # Campo ativo

    def __str__(self):
        return self.nome

class EnderecoFornecedor(models.Model):
    fornecedor = models.ForeignKey(Fornecedor, related_name='enderecos', on_delete=models.CASCADE)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.fornecedor.nome} - {self.endereco}"

class ContatoFornecedor(models.Model):
    fornecedor = models.ForeignKey(Fornecedor, related_name='contatos', on_delete=models.CASCADE)
    contato = models.ForeignKey(Contato, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.fornecedor.nome} - {self.contato}"

class DocumentoFornecedor(models.Model):
    fornecedor = models.ForeignKey(Fornecedor, related_name='documentos_files', on_delete=models.CASCADE)
    documentos = models.ForeignKey(DocumentoFile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.fornecedor.nome} - {self.documentos}"

class FornecedorEmpresa(models.Model):
    empresa = models.ForeignKey(Empresa, related_name='fornecedores', on_delete=models.CASCADE)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.empresa.razao_social} - {self.fornecedor.nome}"

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    documentos = models.ForeignKey(Documento, on_delete=models.CASCADE, null=True, blank=True)
    info_pessoal = models.ForeignKey(InfoPessoal, on_delete=models.CASCADE, null=True, blank=True)
    preferencias = models.TextField(null=True, blank=True)
    observacoes = models.TextField(null=True, blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True)  # Campo ativo

    def __str__(self):
        return self.nome

class EnderecoCliente(models.Model):
    cliente = models.ForeignKey(Cliente, related_name='enderecos', on_delete=models.CASCADE)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.cliente.nome} - {self.endereco}"

class ContatoCliente(models.Model):
    cliente = models.ForeignKey(Cliente, related_name='contatos', on_delete=models.CASCADE)
    contato = models.ForeignKey(Contato, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.cliente.nome} - {self.contato}"

class DocumentoCliente(models.Model):
    cliente = models.ForeignKey(Cliente, related_name='documentos_files', on_delete=models.CASCADE)
    documentos = models.ForeignKey(DocumentoFile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.cliente.nome} - {self.documentos}"

class ClienteEmpresa(models.Model):
    empresa = models.ForeignKey(Empresa, related_name='clientes', on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.empresa.razao_social} - {self.cliente.nome}"

class Colaborador(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, related_name='colaboradores')
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name='colaboradores', null=True, blank=True)
    data_admissao = models.DateField()
    data_demissao = models.DateField(null=True, blank=True)
    documentos = models.ForeignKey(Documento, on_delete=models.CASCADE, null=True, blank=True)
    info_pessoal = models.ForeignKey(InfoPessoal, on_delete=models.CASCADE, null=True, blank=True)
    info_bancaria = models.ForeignKey(InfoBancaria, on_delete=models.CASCADE, null=True, blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True)  # Campo ativo
    acesso = models.BooleanField(default=False)  # Campo acesso

    def __str__(self):
        return self.nome

class EnderecoColaborador(models.Model):
    colaborador = models.ForeignKey(Colaborador, related_name='enderecos', on_delete=models.CASCADE)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.colaborador.nome} - {self.endereco}"

class ContatoColaborador(models.Model):
    colaborador = models.ForeignKey(Colaborador, related_name='contatos', on_delete=models.CASCADE)
    contato = models.ForeignKey(Contato, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.colaborador.nome} - {self.contato}"

class DocumentoColaborador(models.Model):
    colaborador = models.ForeignKey(Colaborador, related_name='documentos_files', on_delete=models.CASCADE)
    documentos = models.ForeignKey(DocumentoFile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.colaborador.nome} - {self.documentos}"

class ColaboradorEmpresa(models.Model):
    empresa = models.ForeignKey(Empresa, related_name='colaboradores', on_delete=models.CASCADE)
    colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.empresa.razao_social} - {self.colaborador.nome}"

class Transportadora(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=15)
    documentos = models.ForeignKey(Documento, on_delete=models.CASCADE, null=True, blank=True)
    info_pessoal = models.ForeignKey(InfoPessoal, on_delete=models.CASCADE, null=True, blank=True)
    veiculos = models.ForeignKey(Veiculo, on_delete=models.CASCADE, null=True, blank=True, related_name='veiculos')
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True)  # Campo ativo

    def __str__(self):
        return self.nome

class EnderecoTransportadora(models.Model):
    transportadora = models.ForeignKey(Transportadora, related_name='enderecos', on_delete=models.CASCADE)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.transportadora.nome} - {self.endereco}"

class ContatoTransportadora(models.Model):
    transportadora = models.ForeignKey(Transportadora, related_name='contatos', on_delete=models.CASCADE)
    contato = models.ForeignKey(Contato, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.transportadora.nome} - {self.contato}"

class DocumentoTransportadora(models.Model):
    transportadora = models.ForeignKey(Transportadora, related_name='documentos_files', on_delete=models.CASCADE)
    documentos = models.ForeignKey(DocumentoFile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.transportadora.nome} - {self.documentos}"

class TransportadoraEmpresa(models.Model):
    empresa = models.ForeignKey(Empresa, related_name='transportadoras', on_delete=models.CASCADE)
    transportadora = models.ForeignKey(Transportadora, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.empresa.razao_social} - {self.transportadora.nome}"

# Signal para criar acesso ao sistema para colaboradores
@receiver(post_save, sender=Colaborador)
def create_colaborador_access(sender, instance, created, **kwargs):
    User = get_user_model()
    if instance.acesso and created:
        # Criar o usuário no sistema
        user = User.objects.create_user(
            username=instance.nome,
            password='defaultpassword',  # Defina uma senha padrão ou gere uma aleatória
            tenant=instance.empresa.tenant,  # Associe ao tenant correto
            nome=instance.nome
        )
    elif not instance.acesso and not created:
        # Desativar o usuário do sistema
        try:
            user = User.objects.get(username=instance.nome)
            user.is_active = False
            user.save()
        except User.DoesNotExist:
            pass