-- Module:Semiconductor
-- Reusable, deterministic educational model; NOT measured device parameters.
-- Input: ionized dopant densities Na, Nd and intrinsic carrier density ni in cm^-3,
-- temperature in K. Conditions: uniform abrupt homojunction, equilibrium,
-- nondegenerate statistics, complete ionization, ni appropriate to T,
-- Na and Nd both much greater than ni.
--
-- The module does not store SMW assertions, query Cargo, reach outside MediaWiki,
-- or infer a material's physical parameters automatically.

local p = {}
local q = 1.602176634e-19        -- elementary charge, C (SI exact)
local kB = 1.380649e-23          -- Boltzmann constant, J/K (SI exact)

local function parsePositive(args, key)
    local x = tonumber(args[key])
    if not x or x ~= x or x == math.huge or x == -math.huge or x <= 0 then
        return nil, key .. " must be a finite positive numeric parameter"
    end
    return x, nil
end

function p.idealJunction(frame)
    local a = frame.args
    local Na, err = parsePositive(a, "Na")
    if err then return "''Model input error: " .. err .. "''" end
    local Nd
    Nd, err = parsePositive(a, "Nd")
    if err then return "''Model input error: " .. err .. "''" end
    local ni
    ni, err = parsePositive(a, "ni")
    if err then return "''Model input error: " .. err .. "''" end
    local T
    T, err = parsePositive(a, "T")
    if err then return "''Model input error: " .. err .. "''" end

    -- Physically necessary for the intended idealized nondegenerate example.
    if T < 50 or T > 600 then
        return "''Model out of scope: temperature outside the illustrative 50–600 K range.''"
    end
    if Na / ni < 100 or Nd / ni < 100 then
        return "''Model out of scope: both doping densities must exceed ni by at least 100-fold.''"
    end

    -- Algebra is done as sums of logarithms to avoid overflow in Na*Nd/(ni*ni).
    local thermal = kB * T / q
    local logratio = math.log(Na / ni) + math.log(Nd / ni)
    local vbi = thermal * logratio
    if vbi ~= vbi or vbi == math.huge or vbi <= 0 then
        return "''Model out of scope: calculated potential is not finite and positive.''"
    end

    -- No derived material parameters: ni is an explicit, temperature-matched input.
    return string.format(
        "''Ideal abrupt homojunction example:'' " ..
        "at T = %.1f K, N_A = %.3g cm<sup>−3</sup>, " ..
        "N_D = %.3g cm<sup>−3</sup> and n_i = %.3g cm<sup>−3</sup>, " ..
        "the thermal voltage k<sub>B</sub>T/q = %.5f V, and the " ..
        "equilibrium built-in potential V<sub>bi</sub> = %.4f V. " ..
        "Assumes nondegenerate equilibrium, fully ionized dopants, uniform " ..
        "abrupt homojunction and a physically appropriate n_i(T); this is " ..
        "not a measured or universal terminal turn-on voltage.",
        T, Na, Nd, ni, thermal, vbi
    )
end

return p
