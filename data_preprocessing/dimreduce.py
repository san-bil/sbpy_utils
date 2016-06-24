from sklearn.decomposition import PCA

def pca_reduce(Y,num_components):
    pca = PCA(n_components=num_components)
    pca.fit(Y)
    return pca.components_