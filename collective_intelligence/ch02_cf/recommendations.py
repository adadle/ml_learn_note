# coding=utf8

from math import sqrt

# A dictionary of movie critics and their ratings of a small
# set of movies
critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
     'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
      'The Night Listener': 3.0},
      'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
           'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
            'You, Me and Dupree': 3.5},
      'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
           'Superman Returns': 3.5, 'The Night Listener': 4.0},
      'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
           'The Night Listener': 4.5, 'Superman Returns': 4.0,
            'You, Me and Dupree': 2.5},
      'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
           'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
            'You, Me and Dupree': 2.0},
      'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
           'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
      'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}

# to calculate euclidean metrics.
def sim_distance(sample, user1, user2):
    intersection = {}
    for item in sample[user1]:
        if item in sample[user2]:
            intersection[item] = 1

    if len(intersection) == 0: return 0
    sum_val = sum([pow(sample[user1][item] - sample[user2][item],2) for item in sample[user1] if item in sample[user2]])
    return 1/(1+sqrt(sum_val))

# to calculate pearson
def sim_pearson(sample, user1, user2):
    si = {}
    for item in sample[user1]:
        if item in sample[user2]:
            si[item] = 1

    n  = len(si)
    if n == 0: return 0
    # sums of all the preferences
    sum1 = sum([sample[user1][it] for it in si])
    sum2 = sum([sample[user2][it] for it in si])
    # sums of all the squares
    sum1sq = sum([pow(sample[user1][it],2) for it in si ])
    sum2sq = sum([pow(sample[user2][it],2) for it in si ])
    # sums of products
    psum = sum([sample[user1][it] * sample[user2][it] for it in si ])
    # Calculate r (Pearson score)
    num=psum-(sum1*sum2/n)
    den=sqrt((sum1sq-pow(sum1,2)/n)*(sum2sq-pow(sum2,2)/n))
    if den==0: return 0
    return num/den

# find reco candidates for user.
def reco_user(sample, userid, pool_size=3, similarity_func=sim_pearson):
    scores = [(similarity_func(sample, cand, userid),cand) for cand in sample if cand != userid]
    scores.sort()
    scores.reverse()
    return scores[0:pool_size]

# find reco moive candidates for user.
def reco_moive(sample, userid, sim_func=sim_pearson):
    totals = {}
    sim_sums = {}
    for cand in sample:
        if cand == userid: continue
        sim = sim_func(sample, userid, cand)
        if sim<=0: continue
        for item in sample[cand]:
            #
            if item not in sample[userid] or sample[userid][item] == 0:
                totals.setdefault(item,0)
                totals[item] += sim * sample[cand][item]
                sim_sums.setdefault(item,0)
                sim_sums[item] += sim

        # 建立归一化
        rankings = [ ( total/sim_sums[item], item) for item,total in totals.items()]
        rankings.sort()
        rankings.reverse()
        return rankings

# item:{item:val,item2:val2}
def transform_items(sample):
    result = {}
    for user in sample:
        for item in sample[user]:
            result.setdefault(item, {})
            result[item][user] = sample[user][item]
    return result

# calculate similar items offline.
def calc_sim_items(item_sample):
    result = {}
    cnt = 0
    for item in item_sample:
        cnt += 1
        if cnt%100 == 0: print 'processed: {0}, total: {1}'.format(cnt, len(item_sample))
        candidates = reco_user(item_sample, item, 5, sim_pearson)
        result[item] = candidates
    return result

#
def reco_item(itemid):
    item_sample = transform_items(critics)
    item_reco_result = calc_sim_items(item_sample)
    return item_reco_result[itemid]



def main():
    # test case
    print reco_user(critics, 'Toby')
    print reco_moive(critics,'Toby') # user-based

    print reco_item('Just My Luck')  # item-based

if __name__ == '__main__':
    main()

