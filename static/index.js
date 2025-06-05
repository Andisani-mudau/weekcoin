fetch('https://weekcoin.onrender.com/tokens')
    .then(res => res.json())
    .then(coins => {
        const sponsoredDiv = document.getElementById('sponsored-coins');
       // const recommendedDiv = document.getElementById('recommended-coins');

        sponsoredDiv.innerHTML = '';
        //recommendedDiv.innerHTML = '';

        const createSponsoredCard = (coin) => `
            <div class="card">
                <div class="card-in">
                    <span class="sponsored">Sponsored</span>
                    <img src="${coin.logo}" alt="${coin.name}" style="object-fit: cover;"/>
                    <div class="card-info-card">
                        <div class="card-info">
                            <h3>$${coin.symbol.toUpperCase()}</h3>
                        </div>
                        <div class="card-usr-inter">
			    <a class="card-buy ui-btn" href="https://pump.fun/coin/${coin.address}" target="_blank">
                                <span>Buy</span>
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        `;

        const createRecommendedCard = (coin) => `
            <div class="card">
                <div class="card-in">
                    <img src="${coin.logo}" alt="${coin.name}" style="object-fit: cover;">
                    <div class="card-info-card">
                        <div class="card-info">
                            <h3>$${coin.symbol.toUpperCase()}</h3>
                        </div>
                        <div class="card-usr-inter">
                            <a class="card-buy ui-btn" href="https://pump.fun/coin/${coin.address}" target="_blank">
                                <span>Buy</span>
                            </a>
                        </div>
                    </div> 
                </div>
            </div>
        `;

        coins.sponsored.forEach(coin => {
            if (coin.error) {
                sponsoredDiv.innerHTML += `<div class="card">${coin.error}</div>`;
                return;
            }
            sponsoredDiv.innerHTML += createSponsoredCard(coin);
        });

        /*coins.recommended.forEach(coin => {
            if (coin && Object.keys(coin).length > 0) {
                if (coin.error) {
                    recommendedDiv.innerHTML += `<div class="card">${coin.error}</div>`;
                    return;
                }
                recommendedDiv.innerHTML += createRecommendedCard(coin);
            }            
        });*/
    })
    .catch(err => {
        document.getElementById('sponsored-coins').innerHTML = `<p style="color:red;">Error: ${err.message}</p>`;
        //document.getElementById('recommended-coins').innerHTML = `<p style="color:red;">Error: ${err.message}</p>`;
    });
