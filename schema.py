from marshmallow import Schema, fields as m_fields


class MetaTagRequestSchema(Schema):
    url = m_fields.URL(required=True)
    meta_tag_name = m_fields.Str(required=True)


class DNSTxtCheckSchema(Schema):
    url = m_fields.URL(required=True)
    txt_record = m_fields.Str(required=True)
