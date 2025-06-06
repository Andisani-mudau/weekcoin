fetch('https://weekcoin.onrender.com/tokens')
    .then(res => res.json())
    .then(coins => {
        const sponsoredDiv = document.getElementById('sponsored-coins');

        sponsoredDiv.innerHTML = '';

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

        coins.sponsored.forEach(coin => {
            if (coin.error) {
                sponsoredDiv.innerHTML += `<div class="card">${coin.error}</div>`;
                return;
            }
            sponsoredDiv.innerHTML += createSponsoredCard(coin);
        });
    })
    .catch(err => {
        document.getElementById('sponsored-coins').innerHTML = `<div class="loader1">
                                                                    <span class="n">N</span>
                                                                    <span class="o">O</span>
                                                                    <span class="t">T</span>
                                                                    <span class="h">H</span>
                                                                    <span class="i">I</span>
                                                                    <span class="n2">N</span>
                                                                    <span class="g">G</span>
                                                                    <span class="d1">.</span>
                                                                    <span class="d2">.</span>
                                                                </div>`;
    });
