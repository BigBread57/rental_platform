import json

from rest_framework import parsers


class MultiPartJSONParser(parsers.MultiPartParser):

    def parse(self, stream, media_type=None, parser_context=None):
        parsed_data = super().parse(stream, media_type=media_type, parser_context=parser_context)

        data = json.loads(parsed_data.data.get('data', '{}'))

        return parsers.DataAndFiles(data=data, files=parsed_data.files)
