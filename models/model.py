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
