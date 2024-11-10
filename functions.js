class Player{
    static AllUsers={}
    constructor(Username){
        this.Username=Username;
        this.Score=0;
        this.correctGuesses=0;
        this.totalGuesses=0;
        this.streak=0;
        Player.AllUsers[Username]=this;
    }
    static getPlayerByName(Username){
        return Player.AllUsers[Username];
    }
    static updatePlayer(Username,Score,Correct ){
        user=this.getPlayerByName(Username);

        if (user){
            user.totalGuesses+=1;

            if(Correct){
                user.Score+=Score;
                user.streak+=1;
                user.correctGuesses+=1

            }
            else{
                user.streak=0
            }
        }

    }

    static allPlayers(){
        return Object.keys(this.AllUsers)
    }

}  