from tortoise import Model, fields


class FileGroup(Model):
    id = fields.IntField(pk=True)
    group_name = fields.CharField(max_length=255)
    group_uuid = fields.CharField(max_length=255)
    create_time = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "tb_file_group"


class FileRecord(Model):
    id = fields.IntField(pk=True)
    file_name = fields.CharField(max_length=255, null=True)
    file_type = fields.CharField(max_length=255, null=True)
    group_id = fields.IntField(null=True)
    create_time = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "tb_file_record"


class ModelTemplate(Model):
    id = fields.IntField(pk=True)
    type = fields.IntField()
    name = fields.CharField(max_length=255)
    alias = fields.CharField(max_length=255, null=True)

    class Meta:
        table = "tb_model_templates"


class EmbeddingModelParameter(Model):
    id = fields.IntField(pk=True)
    model_template_id = fields.IntField(description="逻辑外建，模型模版")
    model_key = fields.CharField(max_length=255)
    model_url = fields.CharField(max_length=255)
    user_id = fields.IntField(description="模型配置所属租户id")

    class Meta:
        table = "tb_embedding_model_parameters"
