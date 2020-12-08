import xlwings as xw
import py_dgm
import pandas as pd
import pkgutil


## to-do:
##  package functions below in one RIAD object instead of individual queries
##  group structure tree should be an attribute of RIAD entity
##  each node should in turn be a RIAD object
##  RIAD object should have MFI attribute (if exists) and contain EA/UC/MPO data

@xw.func
@xw.ret(expand='table')
def get_close_links_by_ids(args):
        
    riad_entity_by_name = pkgutil.get_data('py_dgm', 'templates/riad_close_links.sql').decode()
    # to-do: escape single quote in riad_entity_name:
    sql_query = riad_entity_by_name.format(args[0],args[1])

    mopdb = py_dgm.dbconn()
    results = pd.read_sql(sql_query,mopdb.conn)
    mopdb.conn.close()
    
    return results


@xw.func
@xw.ret(expand='table')
def get_close_linked_assets(args):
        
    riad_entity_by_name = pkgutil.get_data('py_dgm', 'templates/riad_close_links_assets.sql').decode()
    # to-do: escape single quote in riad_entity_name:
    sql_query = riad_entity_by_name.format(args)

    mopdb = py_dgm.dbconn()
    results = pd.read_sql(sql_query,mopdb.conn)
    mopdb.conn.close()
    
    return results
    
def get_entity_by_kwargs(**kwargs):
    if 'RIAD_CODE' not in kwargs or kwargs['RIAD_CODE'] is None: kwargs['RIAD_CODE'] = '#NULL'
    if 'RIAD_NAME' not in kwargs or kwargs['RIAD_NAME'] is None: kwargs['RIAD_NAME'] = '#NULL'
    if 'RIAD_OUID' not in kwargs or kwargs['RIAD_OUID'] is None: kwargs['RIAD_OUID'] = 'NULL'
        
    riad_entity_by_name = pkgutil.get_data('py_dgm', 'templates/riad_entity_by_name.sql').decode()
    # to-do: escape single quote in riad_entity_name:
    sql_query = riad_entity_by_name.format(kwargs["RIAD_CODE"],kwargs["RIAD_NAME"],kwargs["RIAD_OUID"])

    mopdb = py_dgm.dbconn()
    results = pd.read_sql(sql_query,mopdb.conn)
    mopdb.conn.close()
    
    return results


@xw.func
@xw.ret(expand='table')
def get_entity_by_name(riad_entitiy_name):
        
    riad_entity_by_name = pkgutil.get_data('py_dgm', 'templates/riad_entity_by_name.sql').decode()
    # to-do: escape single quote in riad_entity_name:
    sql_query = riad_entity_by_name.format('NULL',riad_entitiy_name,'NULL')

    mopdb = py_dgm.dbconn()
    results = pd.read_sql(sql_query,mopdb.conn)
    mopdb.conn.close()
    
    return results
	


def get_riad_group_by_riad_code(riad_code):
    
    riad_group_by_riad_code = pkgutil.get_data('py_dgm', 'templates/riad_group_by_riad_code.sql').decode()
    # to-do: escape single quote in riad_entity_name:
    sql_query = riad_group_by_riad_code.format(riad_code)
    
    mopdb = py_dgm.dbconn()
    results = pd.read_sql(sql_query,mopdb.conn)
    mopdb.conn.close()
    
    if len(results.index)==0:
        raise Exception("No group information found for RIAD code '{}'".format(riad_code)) 
    
    return    results

@xw.func
def get_head_of_riad_code(riad_entity_code):
    
    riad_head_of_riad_code = pkgutil.get_data('py_dgm', 'templates/riad_head_of_riad_code.sql').decode()
    # to-do: escape single quote in riad_entity_name:
    sql_query = riad_head_of_riad_code.format(riad_entity_code)
    
    mopdb = py_dgm.dbconn()
    results = pd.read_sql(sql_query,mopdb.conn)
    mopdb.conn.close()
    
    return results


def show_tree_of_riad_group(riad_group,mopdb):
    from treelib import Node, Tree
    tree = Tree()
    
    ## combine ORG RIAD codes and GH RIAD codes in one DF
    ##  DF to be used as input to get MFI data
    riad_as_input = riad_group[["ORG_RIAD_CODE","ORG_ORGUNIT_NAME"]].copy()
    tmp = riad_group[["GH_RIAD_CODE","GH_ORGUNIT_NAME"]].copy()
    tmp.rename(columns={"GH_RIAD_CODE":"ORG_RIAD_CODE","GH_ORGUNIT_NAME":"ORG_ORGUNIT_NAME"},inplace=True)
    riad_as_input = riad_as_input.append(tmp)
    riad_as_input.drop_duplicates(inplace=True)
    riad_as_input.reset_index(drop=True,inplace=True)
    
    mfi_obj=mfis(riad_as_input,mopdb)
    mfi_data = mfi_obj.data
    
    #root:
    tree.create_node(   riad_group["GH_ORGUNIT_NAME"][0],
                         riad_group["GH_RIAD_CODE"][0], 
                         data=mfi( mfi_data[mfi_data['RIAD_CODE']==riad_group["GH_RIAD_CODE"][0] ]  )
                    )

    i=0
    for index, row in riad_group.iterrows():
        i=i+1
        #if i==500:
            #tree.show(data_property="summary",  line_type="ascii-em")
            #break
        try:
            tree.create_node(   row["ORG_ORGUNIT_NAME"],
                                row["ORG_RIAD_CODE"],
                                parent=row["DP_RIAD_CODE"], 
                                data=mfi( mfi_data[mfi_data['RIAD_CODE']==row["ORG_RIAD_CODE"] ] )
                            )    
        except:
            missing_dp_id = row["DP_RIAD_CODE"]
            add_missing_node(tree,riad_group,missing_dp_id,mfi_data)
    
    f= open('D:/tree.txt',"w+", encoding="utf8")
    f.write("")
    f.close()
    tree.show(data_property="summary", line_type="ascii-em")
    tree.save2file(filename='D:/tree.txt',data_property="summary", line_type="ascii-em")
    f= open('D:/tree.txt',"r", encoding="utf8")
    contents = f.readlines()
    f.close()
    
    return contents
    #return tree.to_json()

def add_missing_node(tree,riad_group_local,missing_dp_id,mfi_data):
    group_copy = riad_group_local.copy()
    filtered = group_copy.loc[riad_group_local['ORG_RIAD_CODE'] == missing_dp_id]
        
    for index, row in filtered.iterrows():
        try:
            tree.create_node(   row["ORG_ORGUNIT_NAME"],
                                 row["ORG_RIAD_CODE"],
                                 parent=row["DP_RIAD_CODE"], 
                                 data=mfi( mfi_data[ row["ORG_RIAD_CODE"] ] )
                            )   
        except:
            add_missing_node(   tree,
                                 riad_group_local,
                                 row["DP_RIAD_CODE"],
                                 mfi_data)
    
    return

class mfi(object): 
    def __init__(self, mfi_data): 
        self.mfi_name = mfi_data["ORG_ORGUNIT_NAME"].values[0]
        self.mfi_id = mfi_data["ORG_RIAD_CODE"].values[0]
        self.nvo= mfi_data["NVO"].values
        self.cvah=mfi_data["CVAH"].values
        self.mpo=mfi_data["MPO"].values
        self.oc=mfi_data["OC"].values[0]
        
        self.summary = "{} ({})  ".format(self.mfi_name,self.mfi_id)
        
        if mfi_data["MFI_ID"].values[0] is not pd.np.nan:
            self.summary = "{} ({})  >>  EA: {},   UC: {},   MPO: {},   O/C: [{}%]".format(self.mfi_name,self.mfi_id,self.nvo, self.cvah, self.mpo, self.oc)
    

        
class mfis(object): 
    def __init__(self, ids, mopdb): 
        
        self.input=ids
        self.input['RIAD_CODE'] = self.input['ORG_RIAD_CODE']
        
        self.mopdb = mopdb
        self.query_mopdb()
        
        self.data["ID"] = self.data['RIAD_CODE']
        self.data.set_index("ID", inplace=True)
        
        #print(self.data)
    
    def query_mopdb(self):
        
        sql_id_list = "'" + self.input['RIAD_CODE'].str.cat(sep="','") + "'" 
        
        #return
        mfi_collateral = pkgutil.get_data('py_dgm', 'templates/mfis_collateral.sql').decode()
                
        sql_query = mfi_collateral.format(sql_id_list)
        results = pd.read_sql(sql_query,self.mopdb.conn)
        
    
        ##  include over-collateralisaiton as OC = CVAH/MPO; OC=inf if MPO=0 or OC=NaN if MPO=null 
        results["OC"] = results["CVAH"] / results["MPO"] * 100
        
        decimals = pd.Series([1, 1, 1, 1], index=['NVO', 'CVAH', 'MPO', 'OC'])
        results = results.round(decimals)
        
        ## add summary column to df
        results["SUMMARY_LIST"] = results[["MFI_NAME","MFI_ID","NVO","CVAH","MPO","OC"]].values.astype(str).tolist()
        results["SUMMARY"] = results['SUMMARY_LIST'].apply(' // '.join)
        
        ## merge the two dataframes:
        self.data = pd.merge(left=self.input,right=results, left_on='RIAD_CODE',right_on='MFI_ID',how='left')
        
        return

        
class c2d(object):
    def __init__(self,group_nodes): 
        if len(group_nodes)>1:
            q_condition = '(1=2 '
            q_ids = group_nodes.tolist()
            for l in chunks(q_ids,10):
                self.r = " in ('" + "','".join(l) + "')"
                q_condition = q_condition + " or mfi_id " + self.r
            q_condition = q_condition+")"
            #print(q_condition)
        
    
def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]



@xw.func
@xw.ret(expand='table',transpose=True)
def concat_unique(left,right):
    left.extend(right)
    return list(set(left))


@xw.func
@xw.arg('chunk_size', numbers=int, empty=999)
@xw.arg('x', empty='#NA', numbers=int)
@xw.arg('sql_variable', empty='NA')
def sql_in_list(x,sql_variable,chunk_size=999):
    ## make sure all values in list are strings:
    for i in range(0, len(x)): 
        x[i] = str(x[i]) 
    ## chop into chunks of size n: this prevents SQL errors whereby the in-operator can only take 1000 values.
    ##  Therefore, chunks should not be larger than 1000 values.
    x_chunks = chunks(x,chunk_size)
    
    ## for each chunk prepare the SQL in-operator:
    y=[]
    for x_ in x_chunks:
        y.append( sql_variable + " in ('" + "', '".join(x_) + "') " )
    
    ## if there is more than one chunk then combine SQL in-operators with OR and encapsulate in brackets ()
    if len(y)>1:
        y_ = "( " + " or ".join(y) + " )"
    else:
        y_ = y
    
    return y_


@xw.func
@xw.ret(expand='table',transpose=True)
def wrapper_function(args):
    kwargs={}
    #if args[0] is not None: 
    kwargs['RIAD_CODE'] = args[0]
    #if args[1] is not None: 
    kwargs['RIAD_NAME'] = args[1]
    #if args[2] is not None: 
    kwargs['RIAD_OUID'] = args[2]
    accepted_values = ['RIAD_CODE','RIAD_NAME','RIAD_OUID']
    if not any(x in kwargs.keys() for x in accepted_values):
        raise Exception("No argument provided.")
    
    global mopdb
    mopdb = py_dgm.dbconn()
    
    print(" input: {}".format(kwargs))
    
    for k in accepted_values:
        if k not in kwargs.keys() or kwargs[k]==None or kwargs[k]=='':
            if k == 'RIAD_OUID':
                kwargs[k]='null'
            else:
                kwargs[k]='#null'
                
            
    if all(kwargs[x]=='null' for x in accepted_values):
        raise Exception("All arguments are empty.")
    
    entities_found = get_entity_by_kwargs(**kwargs)
            
    if len(entities_found.index)==0:
        raise Exception("No entities found with name like '{}'".format(kwargs))
    elif len(entities_found.index)==1:
        print(" found one match: ({}) {}".format(entities_found["RIAD_CODE"][0],entities_found["RIAD_NAME"][0]))
    elif len(entities_found.index)>1:
        print(" {} matches - defaulting to first match: ({}) {}".format(len(entities_found.index),entities_found["RIAD_CODE"][0],entities_found["RIAD_NAME"][0]))
    
    group_structure = get_riad_group_by_riad_code(entities_found["RIAD_CODE"][0])
    #print(group_structure)
    result_count = len(group_structure.index) +1 #+1 for Group Head
    print(" group contains {0} entities in RIAD.".format(result_count))
    #print(group_structure)
    print("\n\nShowing group results:\n")
    contents = show_tree_of_riad_group(group_structure, mopdb)
    
    mopdb.conn.close()
    return contents
            
    

def user_query():
    user_in={}
    user_in['RIAD_NAME'] = input("RIAD name (wildcards allowed: %, _): ")
    user_in['RIAD_CODE'] = input("RIAD code (no wildcards allowed): ")
    user_in['RIAD_OUID'] = input("RIAD OUID (no wildcards allowed): ")
    
    return (user_in)



if __name__ == '__main__':
    
    
    args=['ES2100',None,None]
    
    #kwargs = user_query()
    wrapper_function(args)
    