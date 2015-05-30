function [Cright] = updateCright(Cright,B,X,A)
    
    %This function contracts the mps B and A with the operator X and a
    %tensor Cright. It returns a Dx1xD tensor, where D is the bond
    %dimension of B and A

    if isempty(X), X=reshape(eye(size(B,3)),[1,1,2,2]); end
    
    % contract index 2<->3 from tensor A<->Cright. They have 3 indeces each
    % return a 4-indeces tensor (3 + 3 - 2)
    Cright=contracttensors(A,3,2,Cright,3,3);
    
    % contract indeces [2,4]<->[4,2] from tensor X<->Cright(output above). 
    %They have 4 indeces each
    % return a 4-indeces tensor (4 + 4 - 4)
    Cright=contracttensors(X,4,[2,4],Cright,4,[4,2]);
    
    % contract indeces [2,3]<->[4,2] from tensor conj(B)<->Cright(output above). 
    %They have 3 and 4 indeces respectevely 
    % return a 3-indeces tensor (3 + 4 - 4)
    Cright=contracttensors(conj(B),3,[2,3],Cright,4,[4,2]);
end

