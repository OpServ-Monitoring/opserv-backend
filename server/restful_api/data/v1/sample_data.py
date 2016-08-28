from flask_restful import Resource


class SampleData(Resource):
    def get(self, sample_id, sample_id2):
        print(sample_id, sample_id2)
        pass

    def put(self, sample_id):
        pass

    def delete(self, sample_id):
        pass
