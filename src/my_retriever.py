import math


class Retrieve:
    # Create new Retrieve object storing index and termWeighting scheme
    def __init__(self,index, termWeighting):
        self.index = index
        self.termWeighting = termWeighting
        
        
        ## give the terms in all the documents with its count(docid > term >count)
        docid_list = list()
        Doc_dict = {}           # contains (docid > term >count)
        for term in index.keys():
            docid = index[term] 
            docid_list.append(docid.keys())
        
        # get the unique doc ids
        unique = list()
        for docid in docid_list:
            for i in docid:
                if i not in unique:
                    unique.append(i)
                else:
                    pass
        
        for docid in unique:
            Doc_dict[docid] = {}
            for key, value in index.items(): 
                if docid in value.keys():
                    Doc_dict[docid][key]=value[docid]
                else:
                    pass
        
        self.Doc_dict = Doc_dict  
        
        # gives the document frequency for all the terms (terms > doc count)
        dfw_dict = {}
        for key,value in index.items():
            dfw_dict[key] = len(value.keys())
        self.dfw_dict = dfw_dict
        
        D = len(Doc_dict.keys())  # total number of documents
        self.D = D
        
        # to get the dsquare({docid:d**2})
        d2_dict = {}  
        d2 = list()
        for key,value in self.Doc_dict.items():
            d2 = list()
            for count in value.values():
                d2.append(count**2)
            d2_dict[key] = sum(d2)
            
        self.d2_dict = d2_dict
        
        # calculate idf values for all the terms
        idf_dict = {}
        for key, value in Doc_dict.items():
            termsInDoc = Doc_dict[key]
            for term in termsInDoc.keys():
                if term in dfw_dict.keys():
                    dfw = dfw_dict[term]
                    idf = math.log(D/dfw)
                    idf_dict[term] = idf
        
        self.idf_dict = idf_dict        
              
    def getUniqueDocId(ListOfList):  # gives the unique docids for the terms in query 
        unique = list()
        for docid in ListOfList:
            for i in docid:
                if i not in unique:
                    unique.append(i)
                else:
                    pass
        return unique 
    
    # For tf: get the candidate documents in descending order of their similarity value   
    def tf(query,Candidate,Doc_dict,d2_dict):
        similarity = {}
        for i in range (len(Candidate)):
            if Candidate[i] in Doc_dict.keys():
                termsInDoc = Doc_dict[Candidate[i]]  # get the terms in the doc with docid = Candidate[i]
                d_sq = d2_dict[Candidate[i]]
                cosine = Retrieve.get_cosine_tf(query, termsInDoc, d_sq)
                similarity[Candidate[i]] = cosine
        Doc_similarity = sorted(similarity, key=similarity.get, reverse=True)
        return Doc_similarity
    
    # For tf: get the cosine value for the candidate document
    def get_cosine_tf(query, Doc_termCount,d_sq):  
        intersection = set(query.keys()) & set(Doc_termCount.keys())
        numerator = sum([query[x] * Doc_termCount[x] for x in intersection])
        sum1 = d_sq
        denominator = math.sqrt(sum1)
        if not denominator:
            return 0.0
        else:
            return float(numerator) / denominator
    
    # For tf.idf: get the cosine value for the candidate document
    def get_cosine_tf_idf(index,D,query,Doc_termCount,dfw_dict,idf_dict): 
        intersection = set(query.keys()) & set(Doc_termCount.keys())
        numerator = sum([query[x] * idf_dict[x] * Doc_termCount[x] * idf_dict[x] for x in intersection])
        sum1 = sum([(Doc_termCount[x] * idf_dict[x])**2 for x in Doc_termCount.keys()])
        denominator = math.sqrt(sum1)
        if not denominator:
            return 0.0
        else:
            return float(numerator) / denominator
        
    # For tf.idf: get the candidate documents in descending order of their similarity value 
    def tf_idf(query,Candidate,Doc_dict,D,index,dfw_dict,idf_dict):
        similarity = {}
        for i in range (len(Candidate)):
            if Candidate[i] in Doc_dict.keys():
                termsInDoc = Doc_dict[Candidate[i]]  # get the terms in the doc with docid = Candidate[i]
                cosine = Retrieve.get_cosine_tf_idf(index,D,query,termsInDoc,dfw_dict,idf_dict)
                similarity[Candidate[i]] = cosine
        Doc_similarity = sorted(similarity, key=similarity.get, reverse=True)
        return Doc_similarity
    
    # For binary: get the cosine value for the candidate document
    def get_cosine_binary(query, Doc_termCount):
        intersection = set(query.keys()) & set(Doc_termCount.keys())
        numerator = len(intersection)
        sum1 = len(Doc_termCount)
        denominator = math.sqrt(sum1)
        if not denominator:
            return 0.0
        else:
            return float(numerator) / denominator
     
    # For binary: get the candidate documents in descending order of their similarity value 
    def binary(query,Candidate,Doc_dict):
        similarity = {}
        for i in range (len(Candidate)):
            if Candidate[i] in Doc_dict.keys():
                termsInDoc = Doc_dict[Candidate[i]]  # get the terms in the doc with docid = Candidate[i]
                cosine = Retrieve.get_cosine_binary(query, termsInDoc)
                similarity[Candidate[i]] = cosine
        Doc_similarity = sorted(similarity, key=similarity.get, reverse=True)
        return Doc_similarity

                
    # Method performing retrieval for specified query
    def forQuery(self, query):
        docid_list = list()
        
        for term in query: # get the docid for the terms in query
            if term in self.index:
                docid = self.index[term] 
                docid_list.append(docid.keys())
            else:
                pass
    
        Candidate = Retrieve.getUniqueDocId(docid_list)   # gives list of candidate documents for the terms in query
       
        if (self.termWeighting == 'tf'):
            return Retrieve.tf(query,Candidate,self.Doc_dict,self.d2_dict)
        elif (self.termWeighting == 'tfidf'):
            return Retrieve.tf_idf(query,Candidate,self.Doc_dict,self.D,self.index,self.dfw_dict,self.idf_dict)
        elif (self.termWeighting == 'binary'):
            return Retrieve.binary(query,Candidate,self.Doc_dict)
        else:
            return Retrieve.binary(query,Candidate,self.Doc_dict)
        
        
            
        
            
            
            
            
            
            