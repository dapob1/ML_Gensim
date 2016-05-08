__author__ = 'oladapobakare'

import nltk
from gensim.summarization import summarize, keywords
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

job_keywords = {}

class KeywordsFromJob(Resource):
    def get(self, keyword_id):
        return {keyword_id: job_keywords[keyword_id]}

    def put(self, keyword_id):
        job_keywords[keyword_id] = request.form['data']
        print job_keywords[keyword_id]
        #self.getKeywords(job_keywords[keyword_id])
        #return {keyword_id: job_keywords[keyword_id]}
        job_keywords[keyword_id] = self.getKeywords(job_keywords[keyword_id])
        #return self.getKeywords(job_keywords[keyword_id])
        return job_keywords[keyword_id]

    def getKeywords(self, jobkeywords):
        myjobkeywords = keywords(jobkeywords, ratio=1)
        revisedkeywords = nltk.word_tokenize(myjobkeywords)
        taggedkeywords = nltk.pos_tag(revisedkeywords)
        nounkeyword = []
        verbkeyword = []

        for element in taggedkeywords:
            if element[1].startswith('NN'):
                nounkeyword.append(element[0])
            elif element[1].startswith('VB'):
                verbkeyword.append(element[0])


        NounsnVerbs = verbkeyword + nounkeyword
        stringofNounsnVerbs = ', '.join(NounsnVerbs)
        print stringofNounsnVerbs
        return stringofNounsnVerbs


api.add_resource(KeywordsFromJob, '/<string:keyword_id>')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    #app.run(debug=True)

